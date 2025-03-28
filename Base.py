
from anthropic import Anthropic
from anthropic.types.message import Message

from typing import Any, Optional, Dict, ClassVar

from openai import OpenAI
import openai


import os
import json

import tools

class AI:
    __model__: str
    __max_tokens__: int = 0

    def __init__(
        self,
        model: Optional[str] = "claude-3-haiku-20240307",
        max_tokens: Optional[int] = 2000,
    ):
        self.__model__ = model
        self.__client__ = Anthropic()
        self.__max_tokens__ = max_tokens

    @property
    def model(self) -> str:
        return self.__model__

    @property
    def model(self, model: str):
        self.__model__ = model

    @property
    def tokens(self) -> int:
        return self.__max_tokens__

    @property
    def tokens(self, tokens: int):
        self.__max_tokens__ = tokens

    def call(self, message: str, stream:Optional[bool]=False, tools: Optional[str] = None) -> Message:
        """call API call to the LLM

        Args:
            message (str): Message that will be send
            tools (_type_): Tools the LLM can use

        Returns:
            any: Returns the response object
        """
        if tools is not None:
            response = self.__client__.messages.create(
                model=self.__model__,
                system="You have access to tools, but only use them when necessary.  If a tool is not required, respond as normal. Don't name the used tool. Answer like as you haven't used a tool",
                max_tokens=self.__max_tokens__,
                messages=message,
                stream=stream,
                tools=tools,
            )
        else:
            response = self.__client__.messages.create(
                model=self.__model__, max_tokens=self.__max_tokens__, messages=message
            )
        return response

    @classmethod
    def load_tools_from_json(self, directory: str) -> list:
        """Load tool definitions from JSON files in a directory."""
        tools = []
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                filepath = os.path.join(directory, filename)
                with open(filepath, "r") as file:
                    tool = json.load(file)
                    tools.append(tool)
        return tools


class OAI:
    """ Class to communicate to chat via OpenAI
    """
    __model__: str
    __max_tokens__: int = 0
    __tools__ : list = None
    __tool_instance__ : tools.Tools = None
    
    def __init__(
        self,
        model: Optional[str] = "gpt-4o-mini",
        max_tokens: Optional[int] = 2000,
    ):
        self.__model__ = model
        self.__client__ = OpenAI()
        self.__max_tokens__ = max_tokens

    @property
    def model(self) -> str:
        return self.__model__

    @property
    def model(self, model: str):
        self.__model__ = model

    @property
    def tokens(self) -> int:
        return self.__max_tokens__

    @property
    def tokens(self, tokens: int):
        self.__max_tokens__ = tokens

    def call(self, message: str, stream:Optional[bool]=False, tools: Optional[str] = None) -> Message:
        """call API call to the LLM

        Args:
            message (str): Message that will be send
            tools (_type_): Tools the LLM can use

        Returns:
            any: Returns the response object
        """
        if tools is not None:
            response  : openai.types.responses.response.Response = self.__client__.responses.create(
                model=self.__model__,
                instructions="You have access to tools, but only use them when necessary.  If a tool is not required, respond as normal. Don't name the used tool. Answer like as you haven't used a tool",
                
                max_output_tokens=self.__max_tokens__,
                input=message,
                tools=tools,
                temperature=0.0
            )
        else:
            response = self.__client__.messages.create(
                model=self.__model__, max_tokens=self.__max_tokens__, messages=message
            )
        return response

    def load_tools_from_json(self, directory: str) -> list:
        """Load tool definitions from JSON files in a directory."""
        tools = []
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                filepath = os.path.join(directory, filename)
                with open(filepath, "r") as file:
                    tool = json.load(file)
                    tools.append(tool)
        self.__tools__ = tools
        return tools
    
    def tool_calls(self, response : openai.types.responses.response.Response ) -> list:
        message : list = [] 
        
        #call tools
        for tool_call in response.output:
            if tool_call.type != "function_call":
                continue

            tool_name = tool_call.name
            args = json.loads(tool_call.arguments)
            if tool_name == "car_calculation":
                result = tools.Tools.car_calculator(**args)
            elif tool_name == 'car_complex_calculation':
                result = tools.Tools.car_complex_calculator(**args)
            
            message.append(tool_call)    
            message.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": str(result)
            })
        return message