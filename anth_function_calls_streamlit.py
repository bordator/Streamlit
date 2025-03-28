from anthropic import Anthropic
from anthropic.types.message import Message

from dotenv import load_dotenv
from tools import Tools

from typing import Any, Optional, Dict, ClassVar
import os
import json

import streamlit as st

import Base


def main():
    
    st.title("Anthrophic-like clone")
    
    # load the enviroment
    load_dotenv()
    # Initialize AI client
    ai = Base.AI()

    tools = None
    if "tools" not in st.session_state:
        # Load tools dynamically from JSON files
        tools_directory = "./tools"  # Directory where JSON files are stored
        tools = ai.load_tools_from_json(tools_directory)
    else:
        tools = st.session_state['tools']

    st.subheader("Tools provided")
    st.code(tools,language='json', wrap_lines=True)

    
    if 'messages' not in st.session_state:
        st.session_state['messages']=[]
        # Define user message
        messages = [
            {
                "role": "user",
                "content": "Please calculate the price for a car which includes the following extras: special wheel and a super battery. ",
            }
        ]
        st.session_state['messages'].append({'role':'user', 'content': messages[0]})
        
    
        # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Call the AI model
    with st.chat_message("assistant"):
        response = ai.call(message=messages, tools=tools)
#        response = st.write_stream(stream)
        st.write(response)
    
    st.session_state["messages"].append({'role':'assistant', 'content':response})
    
    #print("------------1st Response-----------------")
    #print(response)
    #print("------------1st Content-----------------")
    #print(response.content)
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
        messages.append({"role": "assistant", "content": response.content})
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

        messages.append(tool_response)
        print("------------tool Response-----------------")

        print(messages)

        with st.chat_message("assistant"):
            response = ai.call(message=messages, tools=tools)
            st.write(response)
            #Generate the final answer if we finished
            if response.stop_reason ==  "end_turn":
                   
        print("------------2st Response-----------------")

        print(response)
        print(response.content)

    else:
        print("AI Response:", response.content)


if __name__ == "__main__":
    main()
