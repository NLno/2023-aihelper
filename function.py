import os
import requests
import openai
import json
from typing import List, Dict

todo_list = []
def lookup_location_id(location: str):
    url = "https://geoapi.qweather.com/v2/city/lookup"
    params = {
        "location": location,
        "key": "09b8f280cc304d89bc0d51db9dd2efc0"
    }
    response = requests.get(url, params=params)
    location_id = response.json().get('location')[0].get('id')
    return location_id

def get_current_weather(location: str):
    location_id = lookup_location_id(location)
    url = "https://devapi.qweather.com/v7/weather/now"
    params = {
        "key": "09b8f280cc304d89bc0d51db9dd2efc0",
        "location": location_id,
    }
    response = requests.get(url, params=params)
    weather_info = response.json().get('now')
    return weather_info

def add_todo(todo: str):
    todo_list.append(todo)
    output = ""
    for todo_item in todo_list:
        output += "- " + todo_item + "\n"
    return output

def function_calling(messages: List[Dict]):
    openai.api_base = "http://localhost:8080"
    openai.api_key = "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"
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
        {
            "name": "add_todo",
            "description": "Add a todo item to the todo list",
            "parameters": {
                "type": "object",
                "properties": {
                    "todo": {
                        "type": "string",
                        "description": "The todo item to be added"
                    }
                },
                "required": ["todo"]
            }
        },
    ]

    response = openai.ChatCompletion.create(
        model="ggml-openllama.bin",
        messages=messages,
        functions=functions,
        function_call="auto",
    )

    function_content = response["choices"][0]["message"]["function_call"]
    if function_content["function"] == "get_current_weather":
        content = json.loads(function_content["arguments"])["location"]
        weather_info = get_current_weather(content)
        feels_like = weather_info['feelsLike']
        description = weather_info['text']
        humidity = weather_info['humidity']
        result = f"Temperature: {feels_like} Description: {description} Humidity: {humidity}"
        return result

    elif function_content["function"] == "add_todo":
        content = json.loads(function_content["arguments"])["todo"]
        todo_info = content
        result = add_todo(todo_info)
        return result

if __name__ == "__main__":
    messages = [{"role": "user", "content": "What's the weather like in Beijing?"}]
    response = function_calling(messages)
    print(response)

    messages = [{"role": "user", "content": "Add a todo: walk"}]
    response = function_calling(messages)
    print(response)