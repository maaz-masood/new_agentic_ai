# MyCrew Crew

Welcome to the MyCrew Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your API key into the `.env` file**

- Modify `src/my_crew/config/agents.yaml` to define the debate moderator and judge personas
- Modify `src/my_crew/config/tasks.yaml` to define the debate rounds and judging criteria
- Modify `src/my_crew/crew.py` to add your own logic, tools and specific args
- Modify `src/my_crew/main.py` to add custom inputs for your debate topic

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the my_crew Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example now runs a structured expert debate and writes the final judging output to `debate_judgment.md` in the project root.

## Understanding Your Crew

The my_crew Crew is composed of multiple AI agents, each with unique roles, goals, and tools. In this version, one agent produces a multi-round debate transcript and the other agent acts as judge, assigning round winners and a final winner. The task flow is defined in `config/tasks.yaml`, and the agent personas live in `config/agents.yaml`.

## Support

For support, questions, or feedback regarding the MyCrew Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
