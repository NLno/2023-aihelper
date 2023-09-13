import gradio as gr
import os
import time
import json

from chat import chat
from stt import audio2text
from image_generate import image_generate
from mnist import image_classification

# Chatbot demo with multimodal input (text, markdown, LaTeX, code blocks, image, audio, & video). Plus shows support for streaming text.

messages = []
current_file_text = None

def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.update(value="", interactive=False)


def add_file(history, file):
    history = history + [((file.name,), None)]
    return history

def convert_to_messages(history):
    messages = []
    
    for user_utt, assistant_utt in history:
        if user_utt[0].endswith((".wav")):
            content = history[-1][0][0]
            response = audio2text(content)
            messages.append({"role": "user", "content": response})
        elif user_utt[0].endswith((".png")):
            messages.append({"role": "user", "content": f"Pleaseclassify {user_utt[0]}"})
        else:
            messages.append({"role": "user", "content": user_utt})

        messages.append({"role": "assistant", "content": assistant_utt})
        
    return messages

def bot(history):
    messages = convert_to_messages(history)
    print(history)
    print(messages)

    if history[-1][0][0].endswith(".wav"):
        history[-1][1] = ""  # Update the history tuple with an empty response
        response = chat(messages)
        for chunk in response:
            chunk_message = chunk['choices'][0]['delta']['content']
            history[-1][1] += str(chunk_message)
            time.sleep(0.02)
        yield history

    elif history[-1][0][0].endswith((".png")):
        response = image_classification(history[-1][0][0])
        history[-1] = (history[-1][0], response)
        yield history

    elif history[-1][0].startswith("/image"):
        content = history[-1][0].replace("/image", "").strip()
        image_url = image_generate(content)
        response = f"![{content}]({image_url})"
        history[-1] = (history[-1][0], response)  # Update the history tuple with the response
        yield history

    else:
        history[-1][1] = ""  # Update the history tuple with an empty response
        response = chat(messages)
        for chunk in response:
            chunk_message = chunk['choices'][0]['delta']['content']
            history[-1][1] += str(chunk_message)
            time.sleep(0.02)
            yield history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )
        clear_btn = gr.Button('Clear')
        btn = gr.UploadButton("📁", file_types=["image", "video", "audio", "text"])

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot
    )
    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear_btn.click(lambda: messages.clear(), None, chatbot, queue=False)

demo.queue()
demo.launch()
