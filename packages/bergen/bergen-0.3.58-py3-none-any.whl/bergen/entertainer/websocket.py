


from asyncio.futures import Future
from bergen.messages.postman.assign.assign import AssignMessage
from bergen.messages.base import MessageModel
from bergen.messages.utils import expandToMessage
from bergen.messages.host import ActivatePodMessage, DeActivatePodMessage
from bergen.messages.postman.assign import BouncedAssignMessage, BouncedCancelAssignMessage, AssignCriticalMessage, AssignReturnMessage, AssignYieldsMessage, AssignProgressMessage
from bergen.schema import Pod
import json
from bergen.entertainer.base import BaseHelper, BaseHost
import logging
import asyncio
import websockets

import asyncio
try:
    from asyncio import create_task
except ImportError:
    #python 3.6 fix
    create_task = asyncio.ensure_future


logger = logging.getLogger()


class WebsocketHelper(BaseHelper):

    async def pass_yield(self, message: AssignMessage, value):
        yield_message = AssignYieldsMessage(data={"yields": value}, meta={"extensions": message.meta.extensions, "reference": message.meta.reference})
        await self.peasent.send_to_arkitekt(yield_message)

    async def pass_progress(self, message: AssignMessage, value, percentage=None):
        message = f'{percentage if percentage else "--"} : {value}'
        progress_message = AssignProgressMessage(data={"message": value, "level": "INFO"}, meta={"extensions": message.meta.extensions, "reference": message.meta.reference})
        await self.peasent.send_to_arkitekt(progress_message)
        pass

    async def pass_result(self,message: AssignMessage, value):
        return_message = AssignReturnMessage(data={"returns": value}, meta={"extensions": message.meta.extensions, "reference": message.meta.reference})
        await self.peasent.send_to_arkitekt(return_message)

    async def pass_exception(self,message: AssignMessage, exception):
        error_message = AssignCriticalMessage(data={"message": str(exception)}, meta={"extensions": message.meta.extensions, "reference": message.meta.reference})
        await self.peasent.send_to_arkitekt(error_message)


class WebsocketHost(BaseHost):
    helperClass = WebsocketHelper
    ''' Is a mixin for Our Bergen '''

    def __init__(self, host= None, port= None, protocol=None, auto_reconnect=True, auth: dict= None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.websocket_host = host
        self.websocket_port = port
        self.websocket_protocol = protocol
        self.token = auth["token"]
        
        self.auto_reconnect= auto_reconnect
        self.allowed_retries = 2
        self.current_retries = 0


    async def connect(self):
        self.incoming_queue = asyncio.Queue()
        self.outgoing_queue = asyncio.Queue()
        self.tasks = []

        self.startup_task = create_task(self.startup())


    async def disconnect(self) -> str:

        for reference, task in self.assignments.items():
            if not task.done():
                logger.info(f"Cancelling Assignment {task}")
                task.cancel()

        if self.connection: await self.connection.close()

        if self.pending:
            for task in self.pending:
                task.cancel()

        logger.info("Entertainer disconnected")

        
    async def startup(self):
        try:
            await self.connect_websocket()
        except Exception as e:

            logger.error(f"Entertainer Connection failed {e}")
            self.current_retries += 1
            if self.current_retries < self.allowed_retries and self.auto_reconnect:
                sleeping_time = (self.current_retries + 1)
                logger.info(f"Retrying in {sleeping_time} seconds")
                await asyncio.sleep(sleeping_time)
                await self.startup()
            else:
                logger.error("No reconnecting attempt envisioned. Shutting Down!")
                return

        self.consumer_task = create_task(
            self.consumer()
        )

        self.producer_task = create_task(
            self.producer()
        )

        self.worker_task = create_task(
            self.workers()
        )

        done, self.pending = await asyncio.wait(
            [self.consumer_task, self.worker_task, self.producer_task],
            return_when=asyncio.FIRST_EXCEPTION
        )

        logger.error(f"Lost connection inbetween everything :( {[ task.exception() for task in done]}")
        logger.error(f'Reconnecting')

        for task in self.pending:
            task.cancel()

        if self.connection: await self.connection.close()
        self.current_retries = 0 # reset retries after one successfull connection
        await self.startup() # Attempt to ronnect again
        

    async def connect_websocket(self):

        uri = f"{self.websocket_protocol}://{self.websocket_host}:{self.websocket_port}/host/?token={self.token}"
        
        self.connection = await websockets.client.connect(uri)
        logger.info("Connecting as Entertainer")


    async def consumer(self):
        logger.warning(" [x] Awaiting Entertaining Calls")
        async for message in self.connection:
            logger.info(f"Incoming {message}")
            await self.incoming_queue.put(message)


    async def producer(self):
        while True:
            message = await self.outgoing_queue.get()
            await self.connection.send(message.to_channels())


    async def send_to_arkitekt(self, message: MessageModel):
        await self.outgoing_queue.put(message)
       

    def raise_exception(self, future: Future):
        if future.exception():
            raise future.exception()

    async def workers(self):
        while True:
            message_str = await self.incoming_queue.get()
            message = expandToMessage(json.loads(message_str))
            logger.info("Received Assignation")

            if isinstance(message, BouncedAssignMessage):
                assert message.data.pod is not None, "Received assignation that had no Pod???"
                assert message.data.pod in self.pod_functions, f"Pod not hosted {message.data.pod} {self.pod_functions}"
                func = self.pod_functions[message.data.pod]
                task = create_task(func(message))
                task.add_done_callback(self.raise_exception)
                self.assignments[message.meta.reference] = task # Run in parallel

            if isinstance(message, BouncedCancelAssignMessage):
                if message.data.reference in self.tasks: 
                    logger.info("Cancellation for task received. Canceling!")
                    task = self.assignments[message.data.reference]
                    if not task.done():
                        task.cancel()
                        logger.warn("Canceled Task!!")
                    else:
                        logger.warn("Task had already finished")
                else:
                    logger.error("Received Cancellation for task that was not in our tasks..")

            
            self.incoming_queue.task_done()


    def check_if_entertain_cancelled(self, id, reference, future):
        # We cancelled the future and now would like to cancel it also on the Arnheim side
        if future.cancelled():
            deactivate = DeActivatePodMessage(data={"pod": id}, meta={"reference": reference})
            self.tasks.append(asyncio.create_task(self.send_to_arkitekt(deactivate)))
            logger.warn(f"Setting Pod inactive {reference}")

    async def deactivatePod(self, id, reference):
        deactivate = DeActivatePodMessage(data={"pod": id}, meta={"reference": reference})
        await self.send_to_arkitekt(deactivate)
        logger.warn(f"Setting Pod inactive {reference}")

    async def activatePod(self, pod: Pod, reference):
        activate = ActivatePodMessage(data={"pod": pod.id}, meta={"reference": reference})
        await self.send_to_arkitekt(activate)


    
    

