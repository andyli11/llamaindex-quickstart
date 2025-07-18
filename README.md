# Multi-agent Research Assistant - Gemini API x LlamaIndex

Use the [Gemini API](https://ai.google.dev/gemini-api/) and [LlamaIndex](https://www.llamaindex.ai/)
to build a multi-agent workflow for a Research Agent.


This app defines a simple agent crew:

- **ResearchAgent**: uses Google Search to gather relevant information.
- **SummarizeAgent**: summarizes the research findings into a concise explanation.

All reasoning is done using Gemini 2.5 Pro. Search is powered by Gemini’s built-in [Google Search Tool](https://ai.google.dev/gemini-api/docs/grounding).


## 🧠 What it does

You ask a question like:
> "What are the key steps in quantum computing?"

The ResearchAgent looks it up via the web, then hands findings to the SummarizeAgent to generate a plain-English summary.


<!-- ## Demo

![Demo of GitHub Resume Generator](assets/demo.gif)

*The app in action: Enter a GitHub username and watch as AI agents research and generate a professional resume* -->

<!-- ## How it works

A crew is defined that follows a short plan:

* Research the user's GitHub profile
* Research any projects from the profile
* Generate a CV/Resume in Markdown format

You can see the CrewAI configuration in [the config
dir](src/github_resume_generator/config/). Also check out the [custom LLM
class](src/github_resume_generator/crew.py) that uses the `google_search` tool
with CrewAI.

The agents all use the Gemini API, by default [Gemini 2.5
Flash](https://ai.google.dev/gemini-api/docs/models#gemini-2.5-flash-preview).
The agent defined for the research task uses the Gemini API's [Google Search
Grounding](https://ai.google.dev/gemini-api/docs/grounding) feature to look up
any relevant information on the supplied user's GitHub profile. This is easy to
implement, runs pretty quickly and can grab any relevant GitHub information from
around the web.

The Crew is wrapped in a FastAPI that serves a streaming endpoint. This API
streams progress updates to indicate as tasks complete, and eventually returns a
message with the resume, in markdown.

The web frontend is just a static HTML page that calls the API and renders
updates. If you want to develop something more complex, the API is serving the
HTML as a static route, so you can deploy a separate web app pointed at the API. -->

## Installation

This project uses [UV](https://docs.astral.sh/uv/) for Python dependency management and package handling.

### Initial setup

First, if you haven't already, install `uv`:

```bash
pipx install uv
```

> [!NOTE]
> Check out the extensive list of [`uv` installation options](https://docs.astral.sh/uv/getting-started/installation/#installation-methods), including instructions for macOS, Windows, Docker and more.

Next, navigate to your project directory and install the dependencies:

```bash
uv sync
```

#### API key

Grab an API key from [Google AI Studio](https://aistudio.google.com/apikey) and
add it to the `.env` file as `GEMINI_API_KEY`.

```bash
cp .env.example .env
# Now edit .env and add add your key to the GEMINI_API_KEY line.
```

You can now choose to run the API service locally.

Run the service. Use `--reload` to automatically refresh while you're editing.

```bash
uv run uvicorn api.service:app --reload
```

With the API server running, browse to http://localhost:8000/

## Disclaimer

This is not an officially supported Google product. This project is not eligible for the [Google Open Source Software Vulnerability Rewards Program](https://bughunters.google.com/open-source-security).

This project is intended for demonstration purposes only. It is not intended for use in a production environment.

