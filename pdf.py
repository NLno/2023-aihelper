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
        # stream=True,
    )
    print("According to the following prompt: ", prompt, "the generated text is: ", response)
    return response['choices'][0]['text']
    
    

def generate_answer(current_file_text: str, content: str):
    if len(content) > 2048:
        content = content[:2048] + "..."
    qustion_prompt = "Now act as a question asker. You should ask a question about " + content\
        + ", based on the following article: " + current_file_text + ", your response should only contain the question that you want to ask."
    return qustion_prompt
    

def generate_summary(current_file_text: str):
    summary_prompt = "Now act as a summarizer. You should summarize the following article: " + current_file_text
    if len(summary_prompt) > 2048:
        summary_prompt = summary_prompt[:2048] + "..."
    return summary_prompt

if __name__ == "__main__":
    prompt = generate_answer("Hello", "Who is Sun Wukong?")
    generate_text(prompt)