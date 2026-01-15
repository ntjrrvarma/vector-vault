import os
import google.generativeai as genai
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

# 1. Load Secrets
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ Error: GEMINI_API_KEY not found in .env file!")

# 2. Setup Google Gemini (The Brain)
genai.configure(api_key=GOOGLE_API_KEY)

# 3. Setup ChromaDB (The Memory)
client = chromadb.PersistentClient(path="chroma_db")

# --- FIX 1: Correct Argument Name & Model ---
# Use 'model_name' (not 'model') and the free embedding model
google_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
    api_key=GOOGLE_API_KEY,
    model_name="models/text-embedding-004"
)

# Create or Get a Collection
collection = client.get_or_create_collection(
    name="code_vault",
    embedding_function=google_ef
)

def add_code_to_memory(filename, code_content):
    """
    Reads code, converts it to numbers (Vectors), and saves to ChromaDB.
    """
    print(f"💾 Memorizing {filename}...", end=" ", flush=True)
    
    collection.add(
        documents=[code_content],
        metadatas=[{"source": filename}],
        ids=[filename]
    )
    print("Done! ✅")

def ask_brain(question):
    """
    Search ChromaDB and ask Gemini.
    """
    print(f"\n🤔 Thinking about: '{question}'...")
    
    # Step A: Search Memory
    results = collection.query(
        query_texts=[question],
        n_results=1
    )
    
    if not results['documents'][0]:
        return "I couldn't find any relevant code in memory."

    retrieved_code = results['documents'][0][0]
    source_file = results['metadatas'][0][0]['source']
    
    print(f"📖 Reading context from: {source_file}")
    
    # Step B: Construct Prompt
    prompt = f"""
    You are a Senior Software Engineer. Explain the following code context to answer the user's question.
    
    CODE CONTEXT ({source_file}):
    {retrieved_code}
    
    USER QUESTION:
    {question}
    
    ANSWER:
    """
    
    # --- FIX 2: Use the Newer Gemini Model ---
    model = genai.GenerativeModel('gemini-flash-latest')
    response = model.generate_content(prompt)
    
    return response.text

# --- Main Execution Block ---
# --- Main Execution Block ---
if __name__ == "__main__":
    # 1. Load your REAL project code
    with open("target_code.py", "r") as f:
        real_code = f.read()
    
    # 2. Feed Memory (We call it "LogSentinel_V1")
    add_code_to_memory("app.py", real_code)
    
    # 3. Ask a TOUGH question about your project
    # Try asking about Redis, Locks, or the Producer logic
    question = "How does the system handle concurrent logs using Redis?"
    
    try:
        answer = ask_brain(question)
        print("\n🤖 AI Answer:")
        print(answer)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")