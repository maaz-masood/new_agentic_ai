import os
from openai import OpenAI
from dotenv import load_dotenv
import gradio as gr
load_dotenv()

openai_key=os.getenv("OPENAI_API_KEY")   
client=OpenAI(api_key=openai_key)


def chat(message, history):
    messages=[ {'role':'system','content':'''You are a personal journal assistant.
    Follow these rules strictly:
    - Respond in 2-3 sentences maximum
    - When asked to pick one option, state the choice and one reason only
    - Never use bullet points or numbered lists
    - Never end with phrases like 'feel free to ask' or 'have a great day'''},
    {'role':'assistant','content':'Hi! How can I help you Today?'}]

    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})




    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
    )
    return response.choices[0].message.content
gr.ChatInterface(
fn=chat,
title="My AI Assistant",
description="Ask me anything!"
).launch()