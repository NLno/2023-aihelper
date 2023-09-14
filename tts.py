import requests
import os
import json
import tempfile
import urllib.parse

def text2audio(content: str):
    url = 'http://localhost:8080/tts'
    headers = {'Content-Type': 'application/json'}
    data = {
        'model': 'en-us-blizzard_lessac-medium.onnx',
        'input': content
    }

    response = requests.post(url, data=json.dumps(data), 
                             headers=headers,
                             )

    if response.status_code == 200:
        file_name = "test_temp.wav"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, file_name)
        
        with open(file_path, 'wb') as f:
            f.write(response.content)

        return file_path   

if __name__ == "__main__":
    text2audio("Sun Wukong (also known as the Great Sage of Qi Tian, Sun Xing Shi, and Dou Sheng Fu) is one of the main characters in the classical Chinese novel Journey to the West")