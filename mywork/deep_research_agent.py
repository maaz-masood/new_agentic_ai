from pydantic import BaseModel
from agents import Agent, Runner, trace, WebSearchTool
import asyncio
import gradio as gr
import os
from dotenv import load_dotenv
load_dotenv()

# Pydantic models
class SearchPlan(BaseModel):
    queries: list[str]

class SearchResult(BaseModel):
    query: str
    findings: str

class ResearchReport(BaseModel):
    title: str
    summary: str
    key_findings: list[str]
    conclusion: str

# Agents
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
    instructions="Synthesize research findings into a comprehensive report in maximum 500 words.",
    model="gpt-4o-mini",
    output_type=ResearchReport
)

# Pipeline
async def deep_research(topic: str) -> ResearchReport:
    plan = await Runner.run(planner_agent, topic)
    queries = plan.final_output.queries        # ← correct assignment

    search_tasks = [Runner.run(search_agent, query) for query in queries]
    results = await asyncio.wait_for(          # ← timeout added
        asyncio.gather(*search_tasks),
        timeout=30.0,
    )
    findings = "\n\n".join([
        f"Query: {r.final_output.query}\nFindings: {r.final_output.findings}"
        for r in results
    ])
    report = await Runner.run(writer, f"Topic: {topic}\n\nFindings:\n{findings}")
    return report.final_output

# Cache
research_cache = {}

# Gradio UI
async def research_ui(topic):
    if topic.lower() in research_cache:
        return research_cache[topic.lower()]
    
    try:
        with trace("Deep Research"):
            report = await deep_research(topic)
            output = f"# {report.title}\n\n"
            output += f"## Summary\n{report.summary}\n\n"
            output += f"## Key Findings\n"
            for finding in report.key_findings:
                output += f"- {finding}\n"
            output += f"\n## Conclusion\n{report.conclusion}"
            research_cache[topic.lower()] = output
            return output
    except Exception as e:
        return f"Research failed: {str(e)}"

import time

research_cache = {}

async def research_ui(topic):
    if topic.lower() in research_cache:
        return research_cache[topic.lower()]
    
    try:
        start = time.time()
        with trace("Deep Research"):
            report = await deep_research(topic)
            elapsed = time.time() - start
            
            output = f"# {report.title}\n\n"
            output += f"## 📋 Summary\n{report.summary}\n\n"
            output += f"## 🔍 Key Findings\n"
            for finding in report.key_findings:
                output += f"- {finding}\n"
            output += f"\n## 🎯 Conclusion\n{report.conclusion}"
            output += f"\n\n---\n⏱ *Research completed in {elapsed:.1f} seconds using 5 parallel searches*"
            
            research_cache[topic.lower()] = output
            return output
    except Exception as e:
        return f"❌ Research failed: {str(e)}"

with gr.Blocks(title="Deep Research Agent", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🔬 Deep Research Agent")
    gr.Markdown("*Powered by GPT-4o-mini • 5 parallel web searches • Real-time data*")
    
    with gr.Row():
        topic_input = gr.Textbox(
            label="Research Topic",
            placeholder="e.g. Impact of AI on healthcare...",
            scale=4
        )
        submit_btn = gr.Button(
            "🔍 Research",
            scale=1,
            variant="primary"
        )
    
    with gr.Row():
        clear_btn = gr.Button("🗑 Clear", scale=1)
    
    output = gr.Markdown(label="Research Report")
    
    gr.Examples(
        examples=[
            ["Impact of AI on healthcare"],
            ["Future of electric vehicles"],
            ["Quantum computing applications"],
        ],
        inputs=topic_input
    )
    
    submit_btn.click(
        fn=research_ui,
        inputs=topic_input,
        outputs=output
    )
    clear_btn.click(
        fn=lambda: ("", ""),
        inputs=None,
        outputs=[topic_input, output]
    )

demo.launch(inbrowser=True)