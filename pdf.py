import os
import re
import openai

def generate_text(prompt):
    # TODO: get prompt, then use text completion API to return the text
    openai.api_base = "http://localhost:8080/v1"
    openai.api_key = "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"
    response = openai.Completion.create(
        model='gpt-3.5-turbo',
        prompt=prompt,
        temperature=0.7,
        stream=True,
    )

    for chunk in response:
        if chunk['choices'][0].get('text'):
            chunk_message = chunk['choices'][0]['text']
            # print("chunk_message:", chunk_message)
            yield str(chunk_message)

    # return response

def generate_answer(current_file_text: str, content: str):
    if len(content) > 2048:
        content = content[:2048] + "..."
    qustion_prompt = "Based on " + current_file_text\
        + ", could you please provide an answer to the following question: " + content
    return qustion_prompt

def generate_summary(current_file_text: str):
    summary_prompt = "Based on " + current_file_text + ", could you provide a brief description of the text?"
    if len(summary_prompt) > 2048:
        summary_prompt = summary_prompt[:2048] + "..."
    return summary_prompt

if __name__ == "__main__":
    #prompt = generate_answer("Hu Tao is a character in Genshin Impact", "Who is Hu Tao?")
    prompt = generate_summary("Sun Wukong is a character in Genshin Impact")
    generate_text("d")