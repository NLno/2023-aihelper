import os

import openai
import requests
import json

def chat(messages):
    openai.api_base = "http://localhost:8080/v1"
    openai.api_key = "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"
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0,
        stream=True,
    )
    return response
