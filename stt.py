import requests
import json

def audio2text(file):
    url = 'http://localhost:8080/v1/audio/transcriptions'

    headers = {"Content-Type": "multipart/form-data"}
    params = {"model": "whisper-1"}
    files = {"file": open(file, "rb")}

    response = requests.post(url, files=files, data=params,
                             #headers = headers
                             )
    
    if response.status_code == 200:
        response_data = json.loads(response.text)
        transcription_text = response_data["text"]
    
    return transcription_text

if __name__ == "__main__":
    transcription = audio2text('sun-wukong.wav')
    print(transcription)