import os
import requests

def image_generate(content: str):
    url = "http://localhost:8080/v1/images/generations"
    headers = {"Content-Type": "application/json"}
    data = {
    "prompt": content,
    "size": "256x256"
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json()["data"][0]["url"])
    return response.json()["data"][0]["url"]

if __name__ == "__main__":
    image_generate('A cute baby sea otter')