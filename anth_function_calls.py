from anthropic import Anthropic
from anthropic.types.message import Message

from dotenv import load_dotenv
from tools import Tools

from typing import Any, Optional, Dict, ClassVar
import os
import json


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

    def call(self, message: str, tools: Optional[str] = None) -> Message:
        """call API call to the LLM

        Args:
            message (str): Message that will be send
            tools (_type_): Tools the LLM can use

        Returns:
            any: Returns the response object
        """
        if tools != None:
            response = self.__client__.messages.create(
                model=self.__model__,
                system="You have access to tools, but only use them when necessary.  If a tool is not required, respond as normal. Don't name the used tool. Answer like as you haven't used a tool",
                max_tokens=self.__max_tokens__,
                messages=message,
                tools=tools,
            )
        else:
            response = self.__client__.messages.create(
                model=self.__model__, max_tokens=self.__max_tokens__, messages=message
            )
        return response


def load_tools_from_json(directory: str) -> list:
    """Load tool definitions from JSON files in a directory."""
    tools = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r") as file:
                tool = json.load(file)
                tools.append(tool)
    return tools


def main():
    # load the enviroment
    load_dotenv()
    # Initialize AI client
    ai = AI(model="claude-3-haiku-20240307")

    # Load tools dynamically from JSON files
    tools_directory = "./tools"  # Directory where JSON files are stored
    tools = load_tools_from_json(tools_directory)

    # Define user message
    message = [
        {
            "role": "user",
            "content": "Please calculate the price for a car which includes the following extras: special wheel and a super battery. ",
        }
    ]

    # Call the AI model
    response = ai.call(message=message, tools=tools)
    print("------------1st Response-----------------")
    print(response)
    print("------------1st Content-----------------")
    print(response.content)
    # Handle the response
    if response.stop_reason == "tool_use":
        # Simulate tool usage
        tool_use = response.content[-1]
        tool_name = tool_use.name
        if tool_name == "car_calculation":
            result = Tools.car_calculator(
                response.content[-1].input["part1"], response.content[-1].input["part2"]
            )
            print(f"Tool result: {result}")
        elif tool_name == "car_complex_calculation":
            paras = response.content[-1].input["parts"]
            result = Tools.car_complex_calculator(paras)
            print(result)

        else:
            print("Unknown tool requested.")

        # Build the answer with the AI
        message.append({"role": "assistant", "content": response.content})
        # Build result message
        tool_response = {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": str(result),
                }
            ],
        }

        message.append(tool_response)
        print("------------tool Response-----------------")

        print(message)
        response = ai.call(message=message, tools=tools)
        print("------------2st Response-----------------")

        print(response)
        print(response.content)

    else:
        print("AI Response:", response.content)


if __name__ == "__main__":
    main()
