

from abc import ABC, abstractmethod
from asyncio.events import AbstractEventLoop

from pydantic.main import BaseModel
from bergen.types.node import ports
from bergen.types.node.ports.ins.int import IntInPort
from bergen.types.node.ports.ins.model import ModelInPort
from bergen.types.node.ports.outs.model import ModelOutPort
from bergen.types.node.ports.outs.int import IntOutPort
from typing import Dict, Tuple, TypedDict, Union
from bergen.utils import ExpansionError, expandInputs, shrinkOutputs
from bergen.messages.assignation import AssignationMessage
from bergen.schema import Template, NodeType
from bergen.constants import ACCEPT_GQL, OFFER_GQL, SERVE_GQL
import logging
import namegenerator
import asyncio
import websockets
from bergen.models import Node, Pod
import inspect
import sys
from aiostream import stream
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import partial
logger = logging.getLogger()
import copy
import json
from bergen.types.model import ArnheimModel

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

    def __init__(self, peasent_helper: BaseHelper, message: AssignationMessage, loop: AbstractEventLoop = None) -> None:
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


    def __init__(self, raise_exceptions_local=False, **kwargs) -> None:
        self.pods = {}
        self.raise_exceptions_local = raise_exceptions_local


        self.nodes_to_register = [] # for Nodes to register
        self.template_function_set = [] # for Templates to register
        self.pod_function_set = [] # For Pods to register

        self.peasent_helper: BaseHelper = self.helperClass(self)

        self.threadpool = ThreadPoolExecutor(5)
        self.processpool = ProcessPoolExecutor(5)

        self.podid_function_map = {}
        self.podid_pod_map = {}


    def register(self, node_template_pod: Union[Node, Template], policy: PodPolicy = MultiplePodPolicy(), **kwargs):

        threaded = kwargs.get("threaded", False)
        expanded = kwargs.get("threaded", True)

        def real_decorator(function):
            is_coroutine = inspect.iscoroutinefunction(function)
            is_asyncgen = inspect.isasyncgenfunction(function)
            is_function = inspect.isfunction(function)


            async def wrapper(message: AssignationMessage):
                
                
                try:
                    kwargs = await expand(node_template_pod,message.data.inputs)

                    if is_coroutine:
                        assignation_helper = AsyncAssignationHelper(self.peasent_helper, message, loop=self.loop)
                        result = await function(assignation_helper, **kwargs)

                        outputs = await shrink(node_template_pod, result)
                        await self.peasent_helper.pass_result(message, outputs)

                        
                    elif is_asyncgen:
                        assignation_helper = AsyncAssignationHelper(self.peasent_helper, message, loop=self.loop)
                        yieldstream = stream.iterate(function(assignation_helper, **kwargs))
                        lastresult = None
                        async with yieldstream.stream() as streamer:
                            async for result in streamer:
                                lastresult = await shrink(node_template_pod, result)
                                await self.peasent_helper.pass_yield(message, lastresult)

                        await self.peasent_helper.pass_result(message, lastresult)

                    elif is_function:  
                        assignation_helper = ThreadedAssignationHelper(self.peasent_helper, message, loop=self.loop)
                        result = await self.loop.run_in_executor(self.threadpool, partial(function,**kwargs), assignation_helper)

                        outputs = await shrink(node_template_pod, result)
                        await self.peasent_helper.pass_result(message, outputs)

                    else:
                        raise NotImplementedError("We do not allow for non async functions right now")

                except Exception as e:
                    await self.peasent_helper.pass_exception(message, e)
                    logger.error(e)
                    if self.raise_exceptions_local: raise e
                
                
                
            
            wrapper.__name__ = function.__name__

            if isinstance(node_template_pod, Node):
                logger.info(f"Registering Template for {node_template_pod.name}")
                self.nodes_to_register.append({
                    "node": node_template_pod,
                    "params": kwargs,
                    "function": wrapper,
                    "policy": policy,
                })

            if isinstance(node_template_pod, Template):
                logger.info(f"Already existing Template that we are providing for {node_template_pod.id}")
                self.template_function_set.append((node_template_pod,wrapper))


            if isinstance(node_template_pod, Pod):
                logger.info(f"Already existing Template that we are providing for {node_template_pod.id}")
                self.pod_function_set.append((node_template_pod,wrapper))



            return wrapper


        return real_decorator



    async def setup_and_run(self):

        logger.info("Offering Our Services as Provider")
        self.peasent = await SERVE_GQL.run_async(ward=self.main_ward, variables = {"name":self.unique_name})
        logger.info("Our Offer was Accesspted")


        async def offer(node: Node = None, params: dict = None, function = None, policy= None):
            peasent_template = await OFFER_GQL.run_async(ward=self.main_ward, variables= {"node": node.id, "params": params, "peasent": self.peasent.id, "policy": policy.dict()})
            return (peasent_template, function)

        logger.info("We are registering our functions as potential Templates")
        template_function_set = await asyncio.gather(*[offer(**values) for values in self.nodes_to_register])

        # We can now combing reigstered templates and already registered templates
        all_templates_function_set =  template_function_set + self.template_function_set


        # Okay 


        logger.info("We are our Pods")
        async def accept(template: Template, function):
            pod = await ACCEPT_GQL.run_async(ward=self.main_ward, variables= {"template": template.id, "peasent": self.peasent.id})
            return (pod, function)


        pod_function_set = await asyncio.gather(*[accept(*values) for values in all_templates_function_set])
       
        # We can now combing registered templates pods and already registerd pods
        all_pod_function_set = pod_function_set + self.pod_function_set

        
        self.templateid_function_map = {value[0].template.id: value[1] for value in all_pod_function_set}
        self.podid_function_map = {value[0].id: value[1] for value in all_pod_function_set}


        logger.info(f"Following functions have been allowed! {[value[1].__name__ for value in all_pod_function_set]}")
        for value in all_pod_function_set:
            logger.info(f"Requesting to host {value[1].__name__} as Pod {value[0].id}" )


        logger.debug("Configuring")
        await self.configure()



    def enable(self, allow_empty_doc=False, widgets={}, policy: PodPolicy = MultiplePodPolicy(), **implementation_details):
        from inspect import signature, Parameter
        from docstring_parser import parse

        def real_decorator(function):

            is_generator = inspect.isasyncgenfunction(function) or inspect.isgenerator(function)
            logger.info(f"Node is {'Generator' if is_generator else 'Function'}")

            sig = signature(function)
            assert "helper" in sig.parameters, "Please provide helper as a first argument to your function"

            # Generate Types from the Annotation
            args = []
            kwargs = []
            function_inputs = sig.parameters
            for key, value in function_inputs.items():

                widget = widgets.get(key, None)

                the_class = value.annotation

                if value.default == Parameter.empty:
                    if issubclass(the_class, ArnheimModel):
                        args.append(ModelInPort.fromParameter(value, the_class, widget=widget))
                    if issubclass(the_class, int):
                        args.append(IntInPort.fromParameter(value, widget=widget))

                else:
                    if issubclass(the_class, ArnheimModel):
                        kwargs.append(ModelInPort.fromParameter(value, the_class, widget=widget))
                    if issubclass(the_class, int):
                        kwargs.append(IntInPort.fromParameter(value, widget=widget))




            # Generate types from the Output
            returns = []

            function_output = sig.return_annotation

            try:

                # Raises type error if we use it with a class but needed here because typing is actually not a class but an Generic Alias :rolling_eyes::
                if function_output._name == "Tuple":
                    for type in function_output.__args__:
                        if issubclass(type, ArnheimModel):
                            returns.append(ModelOutPort(value, key=type.__name__))
                        if issubclass(type, int):
                            returns.append(IntOutPort(key=type.__name__))

            except AttributeError as e:
                # Once here we should have only classes... lets see about that
                if issubclass(function_output, ArnheimModel):
                        returns.append(ModelOutPort(function_output, key=function_output.__name__))
                if issubclass(function_output, int):
                        returns.append(IntOutPort(key=function_output.__name__))
                





            # Docstring Parser to help with descriptions
            docstring = parse(function.__doc__)
            if docstring.long_description is None:
                assert allow_empty_doc is not False, f"We don't allow empty documentation for function {function.__name__}. Please Provide"
                logger.warn(f"Allowing empty Documentatoin. Please consider providing a documentation for function {function.__name__}")


            name = docstring.short_description or function.__name__
            description = docstring.long_description or "No Description"

            doc_param_map = {param.arg_name: {
                "required": not param.is_optional,
                "description": param.description if not param.description.startswith("[") else None,
            } for param in docstring.params}


            if docstring.returns:
                return_description = docstring.returns.description
                seperated_list = return_description.split(",")
                assert len(returns) == len(seperated_list), "Length of Description and Returns not Equal: If you provide a Return Annotation make sure you seperate the description for each port with ','"
                for index, doc in enumerate(seperated_list):
                    returns[index].description = doc

            # TODO: Update with documentatoin.... (Set description for portexample)
            for port in args:
                if port.key in doc_param_map:
                    updates = doc_param_map[port.key]
                    port.description = updates["description"] or port.description

            for port in kwargs:
                if port.key in doc_param_map:
                    updates = doc_param_map[port.key]
                    port.description = updates["description"] or port.description


            logger.info(f"Creating Arg Ports: {[str(port.key) for  port in args]}")
            logger.info(f"Creating Kwargs Ports: {[str(port.key) for  port in kwargs]}")
            logger.info(f"Creating Returns Ports: {[str(port.key) for  port in returns]}")

            node = Node.objects.update_or_create(
                name = name,
                package = self.unique_name,
                interface = function.__name__,
                description = description,
                args = [arg.serialize() for arg in args],
                kwargs = [kwarg.serialize() for kwarg in kwargs],
                returns = [re.serialize() for re in returns],
                type = NodeType.GENERATOR if is_generator else NodeType.FUNCTION
            )


            wrapper = self.register(node, policy=policy, **implementation_details)
            wrapped = wrapper(function)

            return wrapped

        return real_decorator


    @abstractmethod
    async def connect(self) -> str:
        raise NotImplementedError("Please overwrite")

    @abstractmethod
    async def disconnect(self) -> str:
        raise NotImplementedError("Please overwrite")

    async def stop(self):
        await self.disconnect(self)

    async def run_async(self):
        await self.setup_and_run()

    def run(self):
        if self.loop.is_running():
            logger.error("Cannot do this, please await run_asnyc()")
        else:
            task = self.loop.create_task(self.setup_and_run())

            async def _async(task):
                return await asyncio.wait([task])

            self.loop.run_until_complete(_async(task))

        # we enter a never-ending loop that waits for data
        # and runs callbacks whenever necessary.
        

