import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load Env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("🔍 Scanning available AI models for your API Key...\n")

try:
    count = 0
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Found: {m.name}")
            count += 1
    
    if count == 0:
        print("❌ No models found. Check your API Key permissions.")
        
except Exception as e:
    print(f"❌ Error listing models: {e}")