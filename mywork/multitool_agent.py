import os

from dotenv import load_dotenv
import asyncio
from datetime import datetime
import random
import gradio as gr
from agents import Agent, Runner, function_tool

load_dotenv()
openai_key=os.getenv("OPENAI_API_KEY")   

@function_tool
def get_weather(city: str) -> str:
    """Get the weather for a given city"""
    return f"Sunny, 75°F in {city}"

@function_tool
def current_time() -> str:
    """Get the current date and time"""
    return f"The time is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

@function_tool
def tell_joke() -> str:
    """Tell a funny joke"""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why do programmers prefer dark mode? Because light attracts bugs!"
    ]
    return random.choice(jokes)

# Then pass them all as a list
agent = Agent(
    name="Personal Assistant",
    model="gpt-4o-mini",
   
        
    instructions="You are a helpful assistant.",
    tools=[get_weather, current_time, tell_joke]  # ← same comma separated list
)

from agents import Runner



async def chat(message, history):
    result = await Runner.run(agent, message)
    return result.final_output

gr.ChatInterface(
    fn=chat,
    title="Personal Assistant SDK",
    description="Powered by OpenAI Agents SDK"
).launch(inbrowser=True)

