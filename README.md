# Ask Anything: Gemini + LlamaIndex RAG System

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
