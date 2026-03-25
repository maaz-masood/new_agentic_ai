from pydantic import BaseModel
from agents import Agent, Runner, trace
import asyncio
import os
from dotenv import load_dotenv
from agents import WebSearchTool
load_dotenv()


# Planner output
class SearchPlan(BaseModel):
    queries: list[str]  # 5 search queries

# Each search result
class SearchResult(BaseModel):
    query: str
    findings: str

# Final report
class ResearchReport(BaseModel):
    title: str
    summary: str
    key_findings: list[str]
    conclusion: str

planner_agent = Agent(
    name="Planner Agent",
    instructions="Generate exactly 5 targeted search queries for the given research topic.",
    model="gpt-4o-mini",
    output_type=SearchPlan,
)

search_agent = Agent(
    name="Search Agent",
    instructions="Research this query and return detailed findings",
    model="gpt-4o-mini",
    tools=[WebSearchTool(search_context_size="low")],
    output_type=SearchResult,
) 
writer = Agent(
    name="Writer",
    instructions="Synthesize research findings into a comprehensive report",
    output_type=ResearchReport
)

async def deep_research(topic: str) -> ResearchReport:
    """ Run the deep research process """
    plan = await Runner.run(planner_agent, topic)
    queries= plan.final_output.queries

    search_results = [Runner.run(search_agent, query) for query in queries]
    results = await asyncio.gather(*search_results)
    findings = "\n\n".join([f"Query: {r.final_output.query}\nFindings: {r.final_output.findings}" for r in results])
    report = await Runner.run(writer, f"Topic: {topic}\n\nFindings:\n{findings}")
    return report.final_output


import gradio as gr

async def research_ui(topic):
    with trace("Deep Research"):
        report = await deep_research(topic)
        output = f"# {report.title}\n\n"
        output += f"## Summary\n{report.summary}\n\n"
        output += f"## Key Findings\n"
        for finding in report.key_findings:
            output += f"- {finding}\n"
        output += f"\n## Conclusion\n{report.conclusion}"
        return output

gr.Interface(
    fn=research_ui,
    inputs=gr.Textbox(label="Research Topic"),
    outputs=gr.Markdown(label="Research Report"),
    title="Deep Research Agent",
    description="Enter any topic to get a comprehensive research report"
).launch(inbrowser=True)