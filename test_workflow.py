#!/usr/bin/env python3

import sys
import os
sys.path.append('src')

# Import from main.py
from main import *

def test_workflow():
    print("🧪 Testing enhanced RAG workflow...\n")
    
    # Load some sample text
    docs = load_from_type("text", "LBJ was the 36th President of the United States. Lyndon Baines Johnson served from 1963 to 1969.")
    engine = build_query_engine(docs)
    
    # Test query that should be found in text
    print("📝 Testing query about content in text:")
    query1 = "Who was the 36th president?"
    response1 = engine.query(query1)
    print(f"Q: {query1}")
    print(f"A: {response1}")
    print(f"✅ Found in text: {not is_answer_not_found(str(response1))}\n")
    
    # Test query that should NOT be found in text
    print("🔍 Testing query about content NOT in text:")
    query2 = "How old is LeBron James?"
    response2 = engine.query(query2)
    print(f"Q: {query2}")
    print(f"A: {response2}")
    print(f"❌ Not found in text: {is_answer_not_found(str(response2))}")
    
    if is_answer_not_found(str(response2)):
        print("\n🌐 Would trigger Google search fallback!")
        google_result = search_web_with_google(query2)
        print(f"Google search result: {google_result[:200]}..." if len(google_result) > 200 else f"Google search result: {google_result}")
        
        if google_result == "quota_exceeded":
            print("\n⚠️  Google Search quota exceeded. Fallback to Gemini general knowledge:")
            gemini_result = answer_with_gemini(query2)
            print(f"Gemini result: {gemini_result[:200]}..." if len(gemini_result) > 200 else f"Gemini result: {gemini_result}")
        elif google_result.startswith("search_error:"):
            print("\n🤖 Google search error. Fallback to Gemini general knowledge:")
            gemini_result = answer_with_gemini(query2)
            print(f"Gemini result: {gemini_result[:200]}..." if len(gemini_result) > 200 else f"Gemini result: {gemini_result}")

if __name__ == "__main__":
    test_workflow()