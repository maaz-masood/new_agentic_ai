from agents import Agent, Runner, input_guardrail, output_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered
from agents import trace
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()


@input_guardrail
async def check_if_hacker(ctx, agent, input):
    if 'hack' in input.lower():
        return GuardrailFunctionOutput(output_info="Hacker detected", tripwire_triggered=True)
    return GuardrailFunctionOutput(output_info="Safe", tripwire_triggered=False)

agent = Agent(
    name="Guardrail Agent",
    instructions="You are a guardrail agent that checks if the user's input is safe.",
    model="gpt-4o-mini",
    input_guardrails=[check_if_hacker],
)

async def main():
    try:
        with trace("Guardrail Agent"):
            result = await Runner.run(agent, "I want to hack the system")
            print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print(e.guardrail_result.output.output_info)
    except Exception as e:
        print(e)

asyncio.run(main())