

from abc import ABC, abstractmethod
from asyncio.events import AbstractEventLoop
from bergen.messages.postman.assign.assign import AssignMessage
import uuid

from pydantic.main import BaseModel
from bergen.utils import expandInputs, shrinkInputs, shrinkOutputs
from bergen.schema import Template
from bergen.constants import ACCEPT_GQL, OFFER_GQL, SERVE_GQL
import logging
import asyncio
from bergen.models import Node, Pod
import inspect
from aiostream import stream
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import partial


logger = logging.getLogger()

class BaseHelper(ABC):

    def __init__(self, peasent) -> None:
        self.peasent = peasent
        pass

    @abstractmethod
    async def pass_yield(self, message, value):
        pass

    @abstractmethod
    async def pass_progress(self, message, value, percentage=None):
        pass

    @abstractmethod
    async def pass_result(self, message, value):
        pass

    @abstractmethod
    async def pass_exception(self, message, exception):
        pass


class AssignationHelper():

    def __init__(self, peasent_helper: BaseHelper, message: AssignMessage, loop: AbstractEventLoop = None) -> None:
        self.peasent_helper = peasent_helper
        self.message = message
        self.loop = loop
        pass

    @abstractmethod
    def progress(self, value, percentage=None):
        pass



class ThreadedAssignationHelper(AssignationHelper):

    def progress(self, value, percentage=None):
        logger.info(f'{percentage if percentage else "--"} : {value}')
        if self.loop.is_running():
            future = asyncio.run_coroutine_threadsafe(self.peasent_helper.pass_progress(self.message, value, percentage=percentage), self.loop)
            return future.result()
        else:
            self.loop.run_until_complete(self.peasent_helper.pass_progress(self.message, value, percentage=percentage))


class AsyncAssignationHelper(AssignationHelper):

    async def progress(self, value, percentage=None):
        logger.info(f'{percentage if percentage else "--"} : {value}')
        await self.peasent_helper.pass_progress(self.message, value, percentage=percentage)



async def shrink(node_template_pod, outputs):
    kwargs = {}
    if isinstance(node_template_pod, Node):
        kwargs = await shrinkOutputs(node=node_template_pod, outputs=outputs)

    if isinstance(node_template_pod, Template):
        kwargs = await shrinkOutputs(node=node_template_pod.node, outputs=outputs)

    if isinstance(node_template_pod, Pod):
        kwargs = await shrinkOutputs(node=node_template_pod.template.node, outputs=outputs)


    return kwargs



async def expand(node_template_pod, inputs):
    kwargs = {}
    if isinstance(node_template_pod, Node):
        kwargs = await expandInputs(node=node_template_pod, inputs=inputs)

    if isinstance(node_template_pod, Template):
        kwargs = await expandInputs(node=node_template_pod.node, inputs=inputs)

    if isinstance(node_template_pod, Pod):
        kwargs = await expandInputs(node=node_template_pod.template.node, inputs=inputs) 
    return kwargs



threadhelper = None
try: 
    threadhelper = asyncio.to_thread
except:
    logger.warn("Threading does not work below Python 3.9")


class PodPolicy(BaseModel):
    type: str


class OneExlusivePodPolicy(PodPolicy):
    type: str = "one-exclusive"

class MultiplePodPolicy(PodPolicy):
    type: str = "multiple"


class BaseHost:
    ''' Is a mixin for Our Bergen '''
    helperClass = None


    def __init__(self, raise_exceptions_local=False, client = None, loop=None,**kwargs) -> None:
        self.pods = {}
        self.raise_exceptions_local = raise_exceptions_local
        self.loop = loop or asyncio.get_event_loop()
        self.client = client

        self.entertainer_helper: BaseHelper = self.helperClass(self)

        self.threadpool = ThreadPoolExecutor(5)
        self.processpool = ProcessPoolExecutor(5)

        self.pod_functions = {}
        self.entertainments = {}
        self.assignments = {}

        self.tasks = []


    @abstractmethod
    async def connect(self) -> str:
        raise NotImplementedError("Please overwrite")

    @abstractmethod
    async def disconnect(self) -> str:
        raise NotImplementedError("Please overwrite")

    def wrapped(self, pod: Pod, function):
        assert pod.template.node is not None, "Cannot wrap this function for pod if you didn't query template and node inputs"
        is_coroutine = inspect.iscoroutinefunction(function)
        is_asyncgen = inspect.isasyncgenfunction(function)
        is_function = inspect.isfunction(function)   

        async def wrapper(message: AssignMessage):
            logger.info(f"Receiving {message}")

            try:
                args, kwargs = await expandInputs(node=pod.template.node, args=message.data.args, kwargs=message.data.kwargs) 

                combined = {**args, **kwargs}


                if is_coroutine:
                    assignation_helper = AsyncAssignationHelper(self.entertainer_helper, message, loop=self.loop)
                    result = await function(assignation_helper, **combined)

                    outputs = await shrinkOutputs(pod.template.node, result)
                    await self.entertainer_helper.pass_result(message, outputs)

                    
                elif is_asyncgen:
                    assignation_helper = AsyncAssignationHelper(self.entertainer_helper, message, loop=self.loop)
                    yieldstream = stream.iterate(function(assignation_helper, **combined))
                    lastresult = None
                    async with yieldstream.stream() as streamer:
                        async for result in streamer:
                            lastresult = await shrinkOutputs(pod.template.node, result)
                            await self.entertainer_helper.pass_yield(message, lastresult)

                    await self.entertainer_helper.pass_result(message, lastresult)

                elif is_function:  
                    assignation_helper = ThreadedAssignationHelper(self.entertainer_helper, message, loop=self.loop)
                    result = await self.loop.run_in_executor(self.threadpool, partial(function,**combined), assignation_helper)

                    outputs = await shrinkOutputs(pod.template.node, result)
                    await self.entertainer_helper.pass_result(message, outputs)

                else:
                    raise NotImplementedError("We do not allow for non async functions right now")

            except Exception as e:
                if self.raise_exceptions_local: raise e
                await self.entertainer_helper.pass_exception(message, e)
                logger.error(e)
            
        wrapper.__name__ = function.__name__

        return wrapper


    @abstractmethod
    async def activatePod(self):
         raise NotImplementedError("Please overwrite")

    @abstractmethod
    async def deactivatePod(self):
         raise NotImplementedError("Please overwrite")

    def check_if_entertain_cancelled(self, id, reference, future):
        # We cancelled the future and now would like to cancel it also on the Arnheim side
        if future.cancelled():
            self.tasks.append(asyncio.create_task(self.deactivatePod(id, reference)))
            logger.warn(f"Setting Pod inactive {reference}")
        
    async def entertain(self, pod: Pod, function):
        ''' Takes an instance of a pod, asks arnheim to activate it and accepts requests on it,
        cancel this task to unprovide your local implementatoin '''
        assert pod.id not in self.pod_functions, "This pod is already entertained"

        reference = str(uuid.uuid4())
        future = self.loop.create_future()

        print("Reoinsoisenoesin")

        self.entertainments[reference] = future
        try:
            self.pod_functions[str(pod.id)] = self.wrapped(pod, function)
        except Exception as e:
            logger.error(e)

        print("oinoinaoina")
        await self.activatePod(pod, reference)
        future.add_done_callback(partial(self.check_if_entertain_cancelled, pod.id, reference,))

        await future

