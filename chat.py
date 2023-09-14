import openai

def chat(messages):
    openai.api_base = "http://localhost:8080/v1"
    openai.api_key = "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"
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.7,
        stream=True,
    )

    for chunk in response:
        chunk_message = chunk['choices'][0]['delta']['content']
        print("chunk_message:", chunk_message)
        yield str(chunk_message)
    # return response

def chat_nostream(messages):
    openai.api_base = "http://localhost:8080/v1"
    openai.api_key = "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"
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.7,
        # stream=True,
    )
    return response

if __name__ == "__main__":
    # answer = chat_nostream([{'role': 'user', 'content': 'who is sunwukong'},])['choices'][0]['message']['content']
    # print(answer)
    response = chat([{'role': 'user', 'content': 'who is sunwukong'},])
    for chunk in response:
        print("chunk_message:", chunk)
