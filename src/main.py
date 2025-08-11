import sys
import os
import google.generativeai as genai
from google.genai import types
from dotenv import load_dotenv
from llama_index.readers.file import PyMuPDFReader
from llama_index.core.schema import Document
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from PIL import Image

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

Settings.llm = GoogleGenAI(model="gemini-1.5-flash", api_key=os.environ["GEMINI_API_KEY"])
Settings.embed_model = GoogleGenAIEmbedding(
    model_name="text-embedding-004",
    api_key=os.environ["GEMINI_API_KEY"]
)


def get_gemini_llm(multimodal=False):
    model = "gemini-1.5-flash" if multimodal else "gemini-1.5-flash"
    return genai.GenerativeModel(model)


def load_pdf(file_path: str):
    reader = PyMuPDFReader()
    return reader.load(file_path=file_path)


def load_image(image_path: str):
    image = Image.open(image_path)
    prompt = "Extract all readable text from this image."
    gemini = get_gemini_llm(multimodal=True)
    response = gemini.generate_content([prompt, image])
    return [Document(text=response.text)]


def load_text(text: str):
    return [Document(text=text)]


def load_url(url: str):
    reader = SimpleWebPageReader(html_to_text=True)
    return reader.load_data([url])


def load_from_type(input_type: str, value: str):
    if input_type == "pdf":
        return load_pdf(value)
    elif input_type == "image":
        return load_image(value)
    elif input_type == "url":
        return load_url(value)
    elif input_type == "text":
        return load_text(value)
    else:
        raise ValueError(f"Unsupported input type: {input_type}")


def build_query_engine(documents):
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine()


def generate_summary(documents, input_type):
    try:
        combined_text = ""
        for doc in documents:
            combined_text += doc.text + "\n\n"
        
        if len(combined_text.strip()) < 100:
            return combined_text.strip()
        
        gemini = get_gemini_llm()
        
        if input_type == "image":
            prompt = "Provide a brief 2-3 sentence summary of the text extracted from this image:"
        elif input_type == "pdf":
            prompt = "Provide a brief 2-3 sentence summary of this PDF document:"
        elif input_type == "url":
            prompt = "Provide a brief 2-3 sentence summary of this webpage content:"
        elif input_type == "mixed":
            prompt = "Provide a brief 2-3 sentence summary of this combined content from multiple sources:"
        else:
            prompt = "Provide a brief 2-3 sentence summary of this text:"
        
        full_prompt = f"{prompt}\n\n{combined_text[:2000]}..."
        response = gemini.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Could not generate summary: {str(e)}"


def generate_preview(documents, source_description):
    """Generate a brief preview of document content for display."""
    try:
        combined_text = ""
        for doc in documents:
            combined_text += doc.text + "\n\n"
        
        # Truncate to first 300 characters for preview
        preview_text = combined_text.strip()[:300]
        if len(combined_text.strip()) > 300:
            preview_text += "..."
        
        return {
            'source': source_description,
            'text_preview': preview_text,
            'character_count': len(combined_text.strip()),
            'document_count': len(documents)
        }
    except Exception as e:
        return {
            'source': source_description,
            'text_preview': f"Error generating preview: {str(e)}",
            'character_count': 0,
            'document_count': len(documents) if documents else 0
        }


def search_web_with_google(query):
    try:
        google_search_tool = types.Tool(
            google_search=types.GoogleSearch()
        )
        
        llm_with_search = GoogleGenAI(
            model="gemini-1.5-flash",
            api_key=os.environ["GEMINI_API_KEY"],
            generation_config=types.GenerateContentConfig(tools=[google_search_tool])
        )
        
        search_prompt = f"Search the web for: {query}. Provide a concise answer based on the search results."
        response = llm_with_search.complete(search_prompt)
        return str(response)
    except Exception as e:
        error_str = str(e)
        if "429" in error_str and "RESOURCE_EXHAUSTED" in error_str:
            return "quota_exceeded"
        elif "quota" in error_str.lower() or "limit" in error_str.lower():
            return "quota_exceeded"
        else:
            return f"search_error: {error_str}"


def answer_with_gemini(query):
    try:
        gemini = get_gemini_llm()
        response = gemini.generate_content(query)
        return response.text
    except Exception as e:
        return f"Gemini search failed: {str(e)}"


def is_answer_not_found(response_text):
    not_found_phrases = [
        "does not provide",
        "does not give", 
        "does not contain",
        "does not mention",
        "not found in",
        "no information",
        "cannot find",
        "doesn't provide",
        "doesn't give",
        "doesn't contain",
        "doesn't mention",
        "cannot be answered",
        "not available",
        "not provided",
        "from the given",
        "given context",
        "given text",
        "provided text",
        "available in the",
        "insufficient information"
    ]
    response_lower = response_text.lower()
    return any(phrase in response_lower for phrase in not_found_phrases)


def main():
    if len(sys.argv) < 3:
        print("Usage: python src/combined.py [pdf|image|url|text] <file_path|image_path|url|text>")
        return

    input_type = sys.argv[1]
    input_value = sys.argv[2]

    docs = load_from_type(input_type, input_value)
    engine = build_query_engine(docs)

    # Generate and show summary
    print("📄 Processing your content...\n")
    summary = generate_summary(docs, input_type)
    print("📋 Summary:")
    print(f"{summary}\n")
    print("━" * 50)
    print("Ask a question (or type 'exit' or 'quit' to stop):")
    while True:
        try:
            query = input("> ")
            if query.lower() in {"exit", "quit"}:
                print("👋 Goodbye!")
                break
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")
            break
        
        response = engine.query(query)
        print(response)
        
        if is_answer_not_found(str(response)):
            print("\n⚠️  Information not found in the provided text.")
            try:
                web_search = input("Would you like to search the web instead? (y/n): ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                print("\n👋 Goodbye!")
                break
            
            if web_search in ['y', 'yes']:
                print("\n🔍 Searching Google...")
                google_result = search_web_with_google(query)
                
                if google_result == "quota_exceeded":
                    print("⚠️  Google Search quota exceeded. Using Gemini's general knowledge instead...")
                    gemini_result = answer_with_gemini(query)
                    print(f"\n💡 Gemini says: {gemini_result}")
                elif google_result.startswith("search_error:"):
                    print("🤖 Google search encountered an error. Let me try with Gemini's general knowledge...")
                    gemini_result = answer_with_gemini(query)
                    print(f"\n💡 Gemini says: {gemini_result}")
                else:
                    print(f"\n🌐 Google search result: {google_result}")
            print()  # Add spacing


if __name__ == "__main__":
    main()