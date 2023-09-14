import gradio as gr
import os
import time
import json

from chat import chat, chat_nostream
from stt import audio2text
from tts import text2audio
from image_generate import image_generate
from fetch import fetch
from search import search
from pdf import generate_text, generate_answer, generate_summary
from function import function_calling
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

# index=0: add user, index=1, add assistant
def convert_to_messages(history_lastest, index):
    global current_file_text
    
    user_utt = history_lastest[0]
    assistant_utt = history_lastest[1]

    if index == 0:
        if isinstance(user_utt, tuple):
            if user_utt[0].endswith((".wav")):
                response = audio2text(user_utt[0])
                messages.append({"role": "user", "content": response})

            elif user_utt[0].endswith((".png")):
                messages.append({"role": "user", "content": f"Please classify {user_utt[0]}"})

            elif user_utt[0].endswith((".txt")):
                content = user_utt[0]
                with open(content) as f:
                    current_file_text = f.read()
                summary_prompt = generate_summary(current_file_text)
                messages.append({"role": "user", "content": summary_prompt})    
        
        else:
            if user_utt.startswith("/fetch"):
                content = user_utt.replace("/fetch", "").strip()
                response = fetch(content)
                if len(response) > 2048:
                    response = response[:2048] + "..."
                messages.append({"role": "user", "content": response})
            
            elif user_utt.startswith("/file"):
                content = user_utt.replace("/file", "").strip()
                question_prompt = generate_answer(current_file_text, content)
                messages.append({"role": "user", "content": question_prompt})

            elif user_utt.startswith("/function"):
                content = user_utt.replace("/function", "").strip()
                messages.append({"role": "user", "content": content})

            # for search, it will add 3 to messages
            elif user_utt.startswith("/search"):
                content = user_utt.replace("/search", "").strip()
                messages.append({"role": "user", "content": content})

                response = search(content)
                if len(response) > 2048:
                    response = response[:2048] + "..."
                messages.append({"role": "assistant", "content": response})

                search_result = "Now explain what is " + content + ", according to the following search result: " + response
                messages.append({"role": "user", "content": search_result})

            else:
                messages.append({"role": "user", "content": user_utt})

    elif index == 1:
        messages.append({"role": "assistant", "content": assistant_utt})

def bot(history):
    print(history)
    print(history[-1])
    convert_to_messages(history[-1], 0)
    print(messages)

    if history[-1][0][0].endswith(".wav"):
        print("endswith.wav but normal test (for tuple type)")
        history[-1][1] = ""  # Update the history tuple with an empty response
        response = chat(messages)
        for chunk in response:
            history[-1][1] += chunk
            yield history
        convert_to_messages(history[-1], 1)

    elif history[-1][0][0].endswith((".png")):
        print("endswith.png")
        response = image_classification(history[-1][0][0])
        history[-1] = (history[-1][0], response)
        yield history
        convert_to_messages(history[-1], 1)

    elif history[-1][0][0].endswith((".txt")) or history[-1][0].startswith("/file"):
        print("startswith/file or endwith.txt")
        history[-1][1] = ""  # Update the history tuple with an empty response
        tmp_content = messages[-1]['content']
        response = generate_text(tmp_content)
        for chunk in response:
            history[-1][1] += chunk
            yield history
        convert_to_messages(history[-1], 1)

    elif history[-1][0].startswith("/audio"):
        print("startswith/audio")
        filtered_messages = []
        for message in messages:
            if message["role"] == "assistant" and message["content"]:
                message["content"] = message["content"].replace("/audio", "")
            filtered_messages.append(message)

        response = chat_nostream(filtered_messages)
        response_audio = text2audio(response['choices'][0]['message']['content'])
        # html_code = "<audio controls><source src=\"{}\" type=\"audio/wav\"></audio>".format(response_audio)
        history[-1][1] = response_audio,
        yield history
        messages.append({"role": "assistant", "content":response['choices'][0]['message']['content']})

    elif history[-1][0].startswith("/image"):
        print("startswith/image")
        content = history[-1][0].replace("/image", "").strip()
        image_url = image_generate(content)
        response = f"![{content}]({image_url})"
        history[-1] = (history[-1][0], response)  # Update the history tuple with the response
        yield history
        convert_to_messages(history[-1], 1)

    elif history[-1][0].startswith("/function"):
        print("startswith/function")
        tmp_content = messages[-1]
        tmp_list = []
        tmp_list.append(tmp_content)
        response = function_calling(tmp_list)
        history[-1] = (history[-1][0], response)
        yield history
        convert_to_messages(history[-1], 1)

    else:
        print("normal text")
        history[-1][1] = ""  # Update the history tuple with an empty response
        response = chat(messages)
        for chunk in response:
            history[-1][1] += chunk
            yield history
        convert_to_messages(history[-1], 1)
    
    print("end*****************")
    print(messages)

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
