
from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": "Write a one-sentence bedtime story about a unicorn."
        }
    ]
)

print(completion.choices[0].message.content)



client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia"
                }
            },
            "required": [
                "location"
            ],
            "additionalProperties": False
        },
        "strict": True
    }
}]
messages = [{"role": "user", "content": "What is the weather like in Paris today?"}]
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools
)

print(completion.choices[0].message.tool_calls)

import requests
from enum import Enum

class Units(Enum):
    KMH = 1
    MILES = 2

def get_weather(latitude, longitude, units : Units):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']

def get_wind_speed(latitude, longitude, units : Units):
    if units == Units.KMH:
        return 20
    return 10

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters":{
            "type": "object",
            "properties": {
                "longitude":{"type": "string"},
                "latitude":{"type": "string"}, 
                "units":{
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature units",
                    "default": "celsius"
                },
            },
            "required": ["longitude", "latitude", "units"],
            "additionalProperties": False
        },
        "strict": True
    }
},
{
    "type": "function",
    "function": {
        "name": "get_wind_speed",
        "description": "Get the current wind conditions for a given location.",
        "parameters":{
            "type": "object",
            "properties": {
                "longitude":{"type": "number"},
                "latitude":{"type": "number"}, 
                "units":{
                    "type": "string",
                    "enum": ["kmh", "miles"],
                    "description": "wind speed",
                    "default": "kmh"
                },
            },
            "required": ["longitude", "latitude", "units"],
            "additionalProperties": False
        },
        "strict": True
    }
},
]

messages = [{"role": "user", "content": "What is the weather and wind like in Paris today ?"}]
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools
)

print(completion.choices[0].message.tool_calls)
print(completion)
print(completion.choices[0].message)
messages.append(completion.choices[0].message)
print(messages)
import json


def call_functions(name : str, args : any):
    if(name == "get_weather"):
        return get_weather(**args)
    elif (name=='get_wind_speed'):
        return get_wind_speed(**args)

## tool loop
for tool_call in completion.choices[0].message.tool_calls:
    ##put the tool call into an json objet
    func_name = tool_call.function.name
    print(func_name)
    print(tool_call.function.arguments)
    args : any = json.loads(tool_call.function.arguments)
    result = call_functions(func_name, args)
    
    messages.append(
        {
            "role":"tool",
            "tool_call_id": tool_call.id,
            "content": str(result) 
        }
    )    

print(messages)
#messages.append(completion.choices[0].message)
completion2 = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools
)
print(completion2.choices[0].message.content)    
    
    
# tool_call = completion.choices[0].message.tool_calls[0]
# args = json.loads(tool_call.function.arguments)

# result = get_weather(args['latitude'], args['longitude'], args['untis'])
# print(message)
# message.append(completion.choices[0].message)
# message.append(
#     {
#         "role": "tool",
#         "tool_call_id": tool_call.id,
#         "content":str(result)
#     }
#     )

# completion2 = client.chat.completions.create(
#     model="gpt-4o",
#     messages=message,
#     tools=tools
# )

# print(completion2.choices[0].message.content)