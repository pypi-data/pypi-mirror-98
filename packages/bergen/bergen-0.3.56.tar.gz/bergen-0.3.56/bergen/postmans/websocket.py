from asyncio.tasks import ensure_future
from bergen.messages.postman.unprovide import UnProvideMessage
from bergen.messages.postman.cancel_assign import CancelAssignMessage
from typing import Callable
from bergen.messages.postman.provide import ProvideMessage
from bergen.messages.postman.assign import AssignMessage
from bergen.utils import expandOutputs, shrinkInputs
from bergen.messages.assignation import AssignationMessage
from bergen.messages.provision import ProvisionMessage
from bergen.messages.exception import ExceptionMessage
from bergen.messages.types import ASSIGNATION, EXCEPTION, PROVISION
from bergen.messages.base import MessageModel
from bergen.postmans.base import BasePostman
import uuid
import logging
from functools import partial

import asyncio
try:
    from asyncio import create_task
except ImportError:
    #python 3.6 fix
    create_task = asyncio.ensure_future


import websockets
from bergen.schema import AssignationStatus, Node, ProvisionStatus, Template
from bergen.models import Pod



logger = logging.getLogger(__name__)


class NodeException(Exception):
    pass

class PodException(Exception):
    pass



class WebsocketPostman(BasePostman):
    type = "websocket"

    def __init__(self, port= None, protocol = None, host= None, auth= None, **kwargs) -> None:
        self.token = auth["token"]
        self.port = port
        self.protocol = protocol
        self.host = host
        self.connection = None      
        self.channel = None         
        self.callback_queue = ''

        self.uri = f"ws://{self.host}:{self.port}/postman/?token={self.token}"
        self.progresses = {}

        # Retry logic
        self.allowed_retries = 2
        self.current_retries = 0

        # Result and Stream Function
        self.futures = {}
        self.streams = {}   # Are queues that are consumed by tasks
        
        # Progress
        self.progresses = {}  # Also queues
        self.pending = []


        self.assign_routing = "assignation_request"
        super().__init__(**kwargs)

    async def connect(self):
        self.callback_queue = asyncio.Queue()
        self.progress_queue = asyncio.Queue()
        self.send_queue = asyncio.Queue()


        self.tasks = []

        self.startup_task = create_task(self.startup())


    async def disconnect(self):

        for task in self.pending:
            task.cancel()

        if self.connection: await self.connection.close()

        if self.startup_task:
            self.startup_task.cancel()

        logger.info("Postman disconnected")

    async def startup(self):
        try:
            await self.connect_websocket()
        except Exception as e:
            logger.debug(e)
            self.current_retries += 1
            if self.current_retries < self.allowed_retries:
                sleeping_time = (self.current_retries + 1)
                logger.error(f"Connection to Arkitekt Failed: Trying again in {sleeping_time} seconds.")
                await asyncio.sleep(sleeping_time)
                await self.startup()
            else:
                return


        self.receiving_task = create_task(
            self.receiving()
        )

        self.sending_task = create_task(
            self.sending()
        )

        self.callback_task = create_task(
            self.callbacks()
        )


        done, self.pending = await asyncio.wait(
            [self.callback_task, self.receiving_task, self.sending_task],
            return_when=asyncio.FIRST_EXCEPTION
        )

        logger.debug(f"Lost connection inbetween everything :( {[ task.exception() for task in done]}")
        logger.error(f'Trying to reconnect Postman')


        if self.connection: await self.connection.close()
        for task in self.pending:
            task.cancel()

        self.current_retries = 0 # reset retries after one successfull connection
        await self.startup()


    async def connect_websocket(self):
        self.connection = await websockets.client.connect(self.uri)
        logger.info("Successfully connected Postman")
        

    async def receiving(self):
        async for message in self.connection:
            await self.callback_queue.put(message)
    
    async def sending(self):
        while True:
            message = await self.send_queue.get()
            if self.connection:
                await self.connection.send(message.to_channels())
            else:
                raise Exception("No longer connected. Did you use an Async context manager?")

    async def callbacks(self):
        while True:
            message = await self.callback_queue.get()
            try:
                parsed_message = MessageModel.from_channels(message=message)
                correlation_id = parsed_message.meta.reference

                assert correlation_id in self.futures or correlation_id in self.streams , "Received Message that wasn't originaing from our futures or streams"
                # Stream Path

                if correlation_id in self.streams:
                    # It is a stream delage to stream
                    await self.streams[correlation_id].put(parsed_message)

                elif correlation_id in self.futures:
            
                    if parsed_message.meta.type == EXCEPTION: #Protocol Exception assigning to correlation
                        parsed_exception = ExceptionMessage.from_channels(message=message)
                        future = self.futures.pop(parsed_exception.meta.reference)
                        future.set_exception(parsed_exception.toException())


                    elif parsed_message.meta.type == ASSIGNATION: # Assignation Exception
                        parsed_assignation = AssignationMessage.from_channels(message=message)

                        if parsed_assignation.data.status == AssignationStatus.PROGRESS:
                            if correlation_id in self.progresses:
                                self.progresses[correlation_id](parsed_assignation.data.statusmessage) # call the function that is the progress function

                        if parsed_assignation.data.status == AssignationStatus.DONE:
                            if correlation_id in self.progresses:
                                self.progresses.pop(correlation_id)
                            future = self.futures.pop(correlation_id)
                            future.set_result(parsed_assignation.data.outputs)

                        if parsed_assignation.data.status == AssignationStatus.ERROR:
                            if correlation_id in self.progresses:
                                self.progresses.pop(correlation_id)
                            future = self.futures.pop(correlation_id)
                            future.set_exception(NodeException(parsed_assignation.data.statusmessage))

                    elif parsed_message.meta.type == PROVISION:
                        parsed_provision = ProvisionMessage.from_channels(message=message)

                        if parsed_assignation.data.status == ProvisionStatus.DONE:
                            future = self.futures.pop(correlation_id)
                            future.set_result(parsed_provision.data.pod)

                        if parsed_assignation.data.status == ProvisionStatus.ERROR:
                            future = self.futures.pop(correlation_id)
                            future.set_exception(PodException(parsed_assignation.data.statusmessage))
                            

                else:
                    raise Exception("Received something weird", parsed_message )

            except Exception as e:
                logger.error(e)

            self.callback_queue.task_done()


    async def buildAssignMessage(self, reference: str = None, node: Node = None, pod: Pod = None, inputs = None, params= None, with_progress=False):
        assert reference is not None, "Must have a reference"
        assert inputs is not None, "Must have inputs"
        assigned_inputs = await shrinkInputs(node=node, inputs=inputs)
        return AssignMessage(data={
                                    "node": node.id if node else None, 
                                    "pod": pod.id if pod else None, 
                                    "inputs": assigned_inputs, 
                                    "params": dict(params or {}),
                                },
                                meta={
                                    "reference": reference,
                                    "extensions": {
                                        "progress": reference if with_progress else None,
                                        "callback": reference
                                    }
                                })


    async def stream(self, node: Node = None, pod: Pod = None, inputs = None, params= None, on_progress: Callable = None):
        logger.info(f"Creating a Stream")
        reference = str(uuid.uuid4())

        assigned_inputs = await shrinkInputs(node=node, inputs=inputs)
        self.streams[reference] = asyncio.Queue()

        with_progress = False
        if on_progress:
            assert callable(on_progress), "on_progress if provided must be a function/lambda"
            with_progress = True
        
        assign = await self.buildAssignMessage(reference=reference, node=node, pod=pod, inputs=inputs, params=params, with_progress=with_progress)
        await self.send_to_arkitekt(assign)

        while True:
            messagein_stream = await self.streams[reference].get()
            
            parsed_message = AssignationMessage.from_channels(messagein_stream)
            if parsed_message.data.status == AssignationStatus.PROGRESS:
                asyncio.get_event_loop().call_soon_threadsafe(on_progress(parsed_message.data.statusmessage))

            if parsed_message.data.status == AssignationStatus.YIELD:
                yield await expandOutputs(node, outputs=parsed_message.data.outputs)

            if parsed_message.data.status == AssignationStatus.ERROR:
                raise NodeException(parsed_message.data.statusmessage)

            if parsed_message.data.status == AssignationStatus.DONE:
                break

    async def send_to_arkitekt(self,request: MessageModel):
        await self.send_queue.put(request)

    async def assign(self, node: Node = None, pod: Pod = None, inputs = None, params= None, on_progress: Callable = None):
        reference = str(uuid.uuid4()) 
        # Where should we do this?
        future = self.loop.create_future()
        self.futures[reference] = future

        with_progress = False
        if on_progress:
            assert callable(on_progress), "on_progress if provided must be a function/lambda"
            self.progresses[reference] = lambda progress: logger.info(progress) 
            with_progress = True
        
        assign = await self.buildAssignMessage(reference=reference, node=node, pod=pod, inputs=inputs, params=params, with_progress=with_progress)
        await self.send_to_arkitekt(assign)

        future.add_done_callback(partial(self.check_if_assign_cancel, reference))  
        outputs = await future

        return await expandOutputs(node, outputs)


    def check_if_assign_cancel(self, reference, future):
        # We cancelled the future and now would like to cancel it also on the Arnheim side
        if future.cancelled():
            cancel = CancelAssignMessage(data={reference: reference}, meta={reference: reference})
            self.tasks.append(asyncio.create_task(self.send_to_arkitekt(cancel)))
            logger.warn(f"Cancelling Assignation {cancel.data.reference}")

    def check_if_provide_cancel(self, reference, future):
        # We cancelled the future and now would like to cancel it also on the Arnheim side
        if future.cancelled():
            cancel = CancelAssignMessage(data={reference: reference}, meta={reference: reference})
            self.tasks.append(asyncio.create_task(self.send_to_arkitekt(cancel)))
            logger.warn(f"Cancelling Assignation {cancel.data.reference}")


    async def buildProvideMessage(self, reference: str = None, node: Node = None, template: Template = None, params= None, with_progress=False):
        assert reference is not None, "Must have a reference"

        return ProvideMessage(data={
                                    "node": node.id if node else None, 
                                    "template": template.id if template else None, 
                                    "params": dict(params or {}),
                                },
                                meta={
                                    "reference": reference,
                                    "extensions": {
                                        "progress": reference if with_progress else None,
                                        "callback": reference
                                    }
      
                                })


    async def buildUnProvideMessage(self, reference: str = None, pod: Pod = None,  with_progress=False):
        assert pod is not None, "Must have a pod to unprovide"

        return UnProvideMessage(data={
                                    "pod": pod.id , 
                                },
                                meta={
                                    "reference": reference,
                                    "extensions": {
                                        "progress": reference if with_progress else None,
                                        "callback": reference
                                    }

                                })


    async def unprovide(self, pod: Pod= None, on_progress: Callable = None) -> Pod:
        reference = str(uuid.uuid4()) 
        # Where should we do this?
        future = self.loop.create_future()
        self.futures[reference] = future

        with_progress = False
        if on_progress:
            assert callable(on_progress), "on_progress if provided must be a function/lambda"
            self.progresses[reference] = lambda progress: logger.info(progress) 
            with_progress = True
        
        assign = await self.buildUnProvideMessage(reference=reference, pod=pod, with_progress=with_progress)
        await self.send_to_arkitekt(assign)
        result = await future
        return result


    async def provide(self, node: Node = None, template: Template = None , params= None, on_progress: Callable = None) -> Pod:
        reference = str(uuid.uuid4()) 
        # Where should we do this?
        future = self.loop.create_future()
        self.futures[reference] = future

        with_progress = False
        if on_progress:
            assert callable(on_progress), "on_progress if provided must be a function/lambda"
            self.progresses[reference] = lambda progress: logger.info(progress) 
            with_progress = True
        
        assign = await self.buildProvideMessage(reference=reference, node=node, template=template, params=params, with_progress=with_progress)
        await self.send_to_arkitekt(assign)

        future.add_done_callback(partial(self.check_if_provide_cancel, reference))  
        provision = await future

        pod = await Pod.asyncs.get(id=provision.pod)
        return pod
