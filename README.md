# GSoC 2025 — Enhance Gemini API Integrations in OSS Agent Tools

> **Author:** Andy Li  ·  **Mentors:** Paige Bailey, Philipp Schmid  ·  **Program:** Google Summer of Code 2025
---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Week‑by‑Week Journey](#week-by-week-journey)
3. [Technical Highlights (Concise)](#technical-highlights-concise)
4. [Impact & Outcomes](#impact--outcomes)
5. [Challenges & Lessons](#challenges--lessons)
6. [Next Steps](#next-steps)
7. [Acknowledgements](#acknowledgements)
8. [License](#license)

---

## Project Overview

This project set out to make the **Gemini API** feel first‑class in popular **agent frameworks**: easier to adopt, more predictable in production, and better documented. I focused on three pillars:

* **Integration gaps**: Multimodal support, structured outputs, and tool/function calling that behave consistently across libraries.
* **Developer ergonomics**: Clearer quickstarts, repeatable setups, and examples that mirror real agent patterns.
* **Upstream sustainability**: Ship improvements as PRs so they live where developers already work.

The result is a small stack of improvements and guides that help devs go from “hello world” to a robust agent that reasons, calls tools, and handles errors gracefully.

---

## Week by Week Journey

### Community Bonding (early June)

I aligned with mentors on scope, success metrics, and target frameworks. I audited the Gemini docs, AI Studio flows, and the current state of OSS agent ecosystems, then sketched a milestones map balancing breadth (multiple frameworks) with depth (production‑ready patterns).

### Week 1 (Jun 16–20) — Foundations

Set up environments (Python + Node), defined a repeatable project skeleton, and drafted an evaluation rubric: clarity of examples, correctness of structured outputs, tool‑calling reliability, and observability. Mapped “happy paths” for agents and the most common failure modes (timeouts, schema drift, token limits).

### Week 2 (Jun 23–27) — Ecosystem Survey

Compared LangChain/LangGraph, LlamaIndex, CrewAI, Composio, and others through small spikes. Documented rough edges (multimodal inputs, tool binding differences, streaming behavior, and auth ergonomics). Chose a minimal but representative set of use‑cases: routing, RAG, and multi‑agent coordination.

### Week 3 (Jun 30–Jul 4) — Agent Routing Pattern

Implemented a “smart email router” flow as an anchor pattern: classify → act → (optional) human‑in‑the‑loop. Replaced heuristics with model‑guided decisions and defined where tools should be invoked. Added trace hooks to observe latency and tool‑call frequency so changes were measurable.

### Week 4 (Jul 7–11) — Documentation First

Turned spikes into narrative quickstarts and cookbook entries. Tightened prompts and instructions so outputs were schema‑conformant by default. Wrote short “why it works” notes to explain decision boundaries (e.g., when to use Flash vs Pro, when to stream, how to surface actionable errors).

### Week 5 (Jul 14–18) — Upstreaming & Ergonomics

Opened PRs to improve examples and fix small inconsistencies discovered during testing. Standardized environment setup (using `uv` in Python), clarified error messages and key handling, and added checks to reduce common foot‑guns (missing keys, oversized inputs, silent fallbacks).

### Week 6 (Jul 28–Aug 1) — RAG Pipeline

Built a LlamaIndex RAG pipeline with Gemini for embeddings and generation. Focused on retrieval quality and developer experience: sensible chunking defaults, context injection, and a predictable interface for swapping models or vector stores without rewriting the app.

### Week 7 (Aug 4–8) — Hardening

Added guardrails around structured outputs and tool calling; documented retry strategies and when to fail fast. Introduced web‑fallback hooks and key‑usage checks. Wrote pytest coverage for critical paths, plus notes for observability (tracing prompts, tokens, and errors) to speed iteration.

### Week 8 (Aug 11–15) — Shipping & Polish

Packaged the examples into a coherent quickstart, addressed bug reports (memory usage, port conflicts, key validation, file size limits), and smoothed the README/Docs flow so a new dev can complete a full run end‑to‑end without guesswork. Captured learnings and drafted a short blog outline.

---

## Technical Highlights (Concise)

* **Structured output by default**: Schemas for predictable, machine‑readable responses; fewer brittle post‑processing steps.
* **Tool/function calling**: Consistent patterns across libraries with clear “when & how” guidance.
* **Multimodal pipelines**: Text + images/files as first‑class citizens where frameworks support it.
* **Observability**: Tracing prompts, tokens, latencies, and tool‑calls; fast feedback loops.
* **DevX details**: Clean setup, helpful errors, and examples that match real production flows.

---

## Impact & Outcomes

* **Merged PRs**

  * `google-gemini/cookbook#853` — example/docs improvements.
* **Active PRs**

  * `google-gemini/gemini-api-quickstart#28`
  * `google-gemini/crewai-quickstart#6` and `#7`
* **Demo**

  * `andyli11/llamaindex-quickstart` — a runnable app demonstrating RAG with context injection, summarization, key‑usage checks, and tests.

These tighten the feedback loop for developers adopting Gemini in agents—moving friction out of the way so they can ship faster.

---

## Challenges & Lessons

* **Library differences are real**: Tool binding, streaming, and multimodal support vary; the fix is clear, opinionated adapters and examples.
* **Schemas reduce chaos**: Validated outputs minimize retries and hidden bugs.
* **Observability is leverage**: Traces convert “it feels slow” into actionable changes.
* **Docs drift quickly**: Examples must be small, correct, and tested to stay useful.

---

## Next Steps

* Broaden **multimodal** paths (images → video; richer file toolchains).
* Harden **Composio** + Gemini integration and ship an auth‑safe starter.
* Publish **end‑to‑end templates** (LangGraph + HITL inbox + CI tests).
* Turn the README narrative into a short **blog series** for wider reach.

---

## Acknowledgements

Huge thanks to mentors **Paige Bailey** and **Philipp Schmid**, and to OSS maintainers who reviewed PRs and shared guidance throughout.

# Final Project
## Ask Anything: Gemini + LlamaIndex RAG System

A powerful RAG (Retrieval-Augmented Generation) system that combines your documents with web search capabilities, powered by Google's Gemini API and LlamaIndex.

<!-- INSERT_DEMO_VIDEO -->

## 🎯 What it does

Load any content (PDFs, images, URLs, or text) and ask questions about it. When information isn't found in your documents, the system automatically offers to search the web or use Gemini's general knowledge.

**Smart Fallback Chain:**
1. **RAG Search** → Query your loaded documents first
2. **Google Search** → Search the web if information not found (when quota available)
3. **Gemini Direct** → Use Gemini's knowledge as final fallback

## ✨ Key Features

### 🖥️ Web Interface
- **Modern UI**: Clean, responsive design with gradient backgrounds
- **Drag & Drop Upload**: Easy file uploads for PDFs and images
- **Multi-input Support**: Upload files, enter URLs, or paste text
- **Real-time Chat**: Interactive Q&A interface with your documents
- **Session Management**: Restart conversations or add additional context
- **Content Previews**: See what you added with text previews and statistics
- **Visual Feedback**: Animated summary updates and formatted responses

### 🧠 AI Capabilities  
- **Multi-format Support**: PDFs, images, web URLs, and plain text
- **Auto-summarization**: Get a brief summary of your content before Q&A
- **Smart Detection**: Automatically detects when answers aren't in your documents
- **Web Search Integration**: Google Search tool with graceful quota handling
- **Gemini Vision**: OCR text extraction from images
- **100% Gemini**: Uses Gemini for both LLM and embeddings
- **Markdown Formatting**: Properly formatted web search results

## 🚀 Usage

### Web Interface (Recommended)


https://github.com/user-attachments/assets/207b5f9c-7416-4dd4-825e-4f1888c372ba



Start the web server:
```bash
python3 src/app.py
```

Then open your browser to `http://localhost:5000` and enjoy the interactive web interface featuring:

#### 📤 **Content Upload**
- **File Upload**: Drag & drop PDFs and images directly into the browser
- **URL Loading**: Enter any webpage URL to extract and analyze content  
- **Text Input**: Paste or type text content for immediate analysis
- **Multiple Sources**: Combine different content types in one session

#### 💬 **Interactive Chat**
- **Real-time Q&A**: Ask questions and get instant responses
- **Smart Fallback**: Automatic web search when info isn't in your documents
- **Formatted Results**: Clean, readable responses with proper markdown
- **Source Attribution**: See whether answers come from your docs or web search

#### ⚙️ **Advanced Features**
- **Add Context**: Expand your knowledge base during conversations
- **Content Previews**: See exactly what content was added with statistics
- **Session Management**: Restart anytime or build on existing conversations
- **Visual Updates**: Animated feedback when summaries are refreshed

### Command Line Interface

```bash
python3 src/main.py [pdf|image|url|text] <input>
```

**Examples:**
```bash
# Analyze a PDF document
python3 src/main.py pdf "/path/to/document.pdf"

# Extract text from an image and ask questions
python3 src/main.py image "/path/to/screenshot.png"

# Load content from a webpage
python3 src/main.py url "https://example.com/article"

# Analyze plain text
python3 src/main.py text "Your text content here"
```

**Sample Session:**
```
📄 Processing your content...

📋 Summary:
The document discusses artificial intelligence developments and their impact on various industries.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ask a question (or type 'exit' or 'quit' to stop):
> What are the main AI applications mentioned?

The document mentions healthcare, finance, and transportation as key AI applications...

> When was Google DeepMind founded?

⚠️  Information not found in the provided text.
Would you like to search the web instead? (y/n): y

🔍 Searching Google...
💡 Gemini says: Google DeepMind was founded in 2010 by Demis Hassabis, Shane Legg, and Mustafa Suleyman. It was later acquired by Google in 2014 and merged with Google AI's machine learning division in 2023.
```

## 📦 Installation

This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

### Setup

1. **Install UV:**
   ```bash
   pipx install uv
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Configure API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

   Get your API key from [Google AI Studio](https://aistudio.google.com/apikey).

## 🔧 Technical Details

**Frontend:**
- **Web Framework**: Flask with CORS support
- **UI**: Responsive HTML5/CSS3 with JavaScript
- **Design**: Modern gradient styling with animations
- **File Upload**: Secure multipart form handling
- **Session Management**: In-memory storage with UUID sessions

**Backend:**
- **LLM**: Gemini 1.5 Flash via `GoogleGenAI`
- **Embeddings**: Gemini `text-embedding-004` via `GoogleGenAIEmbedding`
- **Vector Store**: LlamaIndex in-memory vector store
- **Search**: Google Search tool (with quota-aware fallback)
- **Vision**: Gemini multimodal for image text extraction

**Supported Formats:**
- **PDF**: PyMuPDFReader for document parsing
- **Images**: PIL + Gemini Vision for OCR
- **URLs**: SimpleWebPageReader for web content
- **Text**: Direct text input

## 🔒 Privacy & Quota

- **Google Search**: Requires quota/billing for web search functionality
- **Quota Handling**: Graceful fallback to Gemini's knowledge when search quota exceeded
- **Data**: All processing uses Google's APIs (see their privacy policies)

## ⚠️ Disclaimer

This is not an officially supported Google product. Intended for demonstration purposes only.
