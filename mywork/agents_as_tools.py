from agents import Agent, Runner, handoff, trace, input_guardrails, GuardrailFunctionOutput
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

researcher = Agent(
    name="Researcher",
    instructions="You research topics and return detailed findings.",
)

summarizer = Agent(
    name="Summarizer",
    instructions="You are given research and summarize it concisely.",
    tools=[researcher.as_tool(
        tool_name="research_topic",
        tool_description="Research a topic in depth and return findings"
    )]
) 
async def main():
    with trace("Agents as Tools Demo"):
        result = await Runner.run(summarizer, "quantum computing")
        print(result.final_output)

asyncio.run(main())