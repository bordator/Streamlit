import openai

from dotenv import load_dotenv
from tools import Tools

from typing import Any, Optional, Dict, ClassVar
import os
import json

import Base


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
    ai = Base.OAI()

    # Load tools dynamically from JSON files
    tools_directory = "./tools/OpenAPI"  # Directory where JSON files are stored
    tools = load_tools_from_json(tools_directory)

    # Define user message
    message = [
        {
            "role": "user",
#            "content": "Please calculate the price for a car which includes the following extras: special wheel,  a super battery and a charger cable. ",
            "content": "What can i do today?",
        }
    ]

    # Call the AI model
    response : openai.types.responses.response.Response = ai.call(message=message, tools=tools)
    
    print("------------1st Response-----------------")
    print(response)
    print("------------1st Content-----------------")
        
    #call tools
    # for tool_call in response.output:
    #     if tool_call.type != "function_call":
    #         continue

    #     tool_name = tool_call.name
    #     args = json.loads(tool_call.arguments)
    #     if tool_name == "car_calculation":
    #         result = Tools.car_calculator(**args)
    #     elif tool_name == 'car_complex_calculation':
    #         result = Tools.car_complex_calculator(**args)
        
    #     message.append(tool_call)    
    #     message.append({
    #         "type": "function_call_output",
    #         "call_id": tool_call.call_id,
    #         "output": str(result)
    #     })
    #Check if we got a response
    if((response.output is not None)):
        tool_response = ai.tool_calls(output=response.output)
        ##Test if there are tool calls needed
        message.extend([*tool_response])
        print("------------tool Response-----------------")
        #check if there was a tool call
        if(len(tool_response) > 0):
            ##Tool call
            print(message)
            response = ai.call(message=message, tools=tools)
            print("------------2st Response-----------------")

        print(response.output_text)
    else:
        print("No Response output !!!!:", response.output_text)


if __name__ == "__main__":
    main()
