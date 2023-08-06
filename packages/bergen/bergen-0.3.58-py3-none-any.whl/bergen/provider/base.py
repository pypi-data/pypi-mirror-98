

from abc import ABC, abstractmethod
from asyncio.events import AbstractEventLoop
from bergen.messages.postman.assign.assign import AssignMessage
from bergen.provider.utils import createNodeFromFunction

from pydantic.main import BaseModel
from bergen.types.node import ports
from bergen.types.node.ports.ins.int import IntInPort
from bergen.types.node.ports.ins.model import ModelInPort
from bergen.types.node.ports.outs.model import ModelOutPort
from bergen.types.node.ports.outs.int import IntOutPort
from typing import Dict, Tuple, TypedDict, Union
from bergen.utils import ExpansionError, expandInputs, shrinkOutputs
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
import uuid



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


class BaseProvider:
    ''' Is a mixin for Our Bergen '''
    helperClass = None


    def __init__(self, *args, name = None, provider: int = None, loop=None, client=None) -> None:
        assert provider is not None, "Provider was set to none, this is weird!!"
        self.arkitekt_provider = provider
        self.name = name
        self.client = client
        self.loop = loop or asyncio.get_event_loop()

        self.template_functions_map = {}
        self.template_on_provide_map = {}

        self.provisions = {}
        self.auto_provided_templates = [] # Templates that this provide will try to provide on startup


    def template(self, node: Node, policy: PodPolicy = MultiplePodPolicy(), auto_provide=False, on_provide=None, **implementation_details):

        def real_decorator(function):
            # TODO: Check if function has same parameters as node
            template = OFFER_GQL.run(
            ward=self.client.main_ward,
            variables= {
                "node": node.id,
                "params": implementation_details,
                "policy": policy.dict()
            })
        
           
            if auto_provide:
                self.auto_provided_templates.append(template)
            if on_provide:
                self.template_on_provide_map[str(template.id)] = on_provide

            

            self.template_functions_map[str(template.id)] = function

            return function

        return real_decorator


    def enable(self, allow_empty_doc=False, widgets={}, **implementation_details):
        """Enables the decorating function as a node on the Arnheim, you will find it as
        @provider/

        Args:
            allow_empty_doc (bool, optional): Allow the enabled function to not have a documentation. Will automatically downlevel the Node Defaults to False.
            widgets (dict, optional): Enable special widgets for the parameters. Defaults to {}.
        """


        assert self.name is not None, "We have no name provided, cannot put created Nodes in a Package without a"
        def real_decorator(function):
            node = createNodeFromFunction(function, self.name, allow_empty_doc=allow_empty_doc, widgets=widgets)
            # We pass this down to our truly template wrapper that takes the node and transforms it
            template_wrapper = self.template(node, **implementation_details)
            function = template_wrapper(function)
            return function

        return real_decorator


    @abstractmethod
    async def connect(self) -> str:
        raise NotImplementedError("Please overwrite")

    @abstractmethod
    async def disconnect(self) -> str:
        raise NotImplementedError("Please overwrite")


    async def run(self):

        #for template in self.auto_provided_templates:
        #    logger.info(f"Autoproviding {template.id}")
        #    # Well cool we can just call ourselfes
        #    task = asyncio.create_task(self.client.postman.provide(template=template))

        logger.info("We are our Pods")

    
    async def provideTemplate(self, reference: str, template_id: str):
        assert template_id in self.template_functions_map, f"There is no function registered for this template {template_id} not it {self.template_functions_map.keys()}"

        if template_id in self.template_on_provide_map:
            self.template_on_provide_map[template_id](reference)
            
        function = self.template_functions_map[template_id]
        pod = await ACCEPT_GQL.run_async(ward=self.client.main_ward, variables= {"template": template_id, "provision": reference})
        print(f"Created {pod}")
        task = asyncio.create_task(self.client.entertainer.entertain(pod, function))
        return pod, task


    async def provide_async(self):
        await self.setup_and_run()

    def provide(self):
        if self.loop.is_running():
            logger.error("Cannot do this, please await run()")
        else:
            task = self.loop.create_task(self.run())
            self.loop.run_forever()

        # we enter a never-ending loop that waits for data
        # and runs callbacks whenever necessary.
        

