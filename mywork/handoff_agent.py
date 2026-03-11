from agents import Agent, Runner, handoff, trace
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
openai_key=os.getenv("OPENAI_API_KEY")

sales_agent = Agent(
    name="Sales Agent",
    instructions="You handle sales queries about pricing and purchasing.",
)

support_agent = Agent(
    name="Support Agent",
    instructions="You handle technical support and troubleshooting.",
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="Route customer queries to the right agent. Use sales agent for pricing questions and support agent for technical issues.",
    handoffs=[sales_agent, support_agent]
)
async def main():
    with trace("Handoff Demo"):
        result = await Runner.run(triage_agent, "I need help with my account.")
        print(result.final_output)

asyncio.run(main())