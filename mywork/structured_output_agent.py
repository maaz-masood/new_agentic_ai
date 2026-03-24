from pydantic import BaseModel
import agents
from agents import Agent, Runner, trace
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

class NewsArticle(BaseModel):
    title: str
    author: str
    summary: str
    source: str
    sentiment: str

agent = Agent(
    name="News Article Agent",
    instructions="You are a news article agent that generates news articles.",
    model="gpt-4o-mini",
    output_type=NewsArticle,
)
async def main():
    with trace("News Article Agent"):
        result = await Runner.run(agent, "Apple just released a new iPhone with revolutionary AI features")
        print(f"Title: {result.final_output.title}")
        print(f"Author: {result.final_output.author}")
        print(f"Summary: {result.final_output.summary}")
        print(f"Source: {result.final_output.source}")
        print(f"Sentiment: {result.final_output.sentiment}")
        
asyncio.run(main())