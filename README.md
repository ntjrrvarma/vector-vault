# 🧠 VectorVault: AI-Powered Internal Developer Platform (IDP)

**VectorVault** is a Retrieval-Augmented Generation (RAG) tool designed to accelerate developer onboarding and legacy code analysis. It allows engineers to chat with their private codebase and architectural documentation (PDFs) using Google Gemini and ChromaDB.

![Status](https://img.shields.io/badge/Status-Production%20Ready-green)
![Tech](https://img.shields.io/badge/AI-Google%20Gemini-blue)
![Stack](https://img.shields.io/badge/Vector%20DB-ChromaDB-orange)

---

## 🚀 Key Features

* **Multi-Modal Ingestion:** Supports analyzing both **Python Source Code (`.py`)** and **Unstructured Documentation (`.pdf`)**.
* **Privacy-First RAG:** Uses a local Vector Database (ChromaDB) to store embeddings; code is sent to the AI only during active queries.
* **Semantic Search:** Finds relevant code blocks based on *meaning*, not just keywords (e.g., searching "Security" finds `auth.py`).
* **Interactive UI:** Built with **Streamlit** for a chat-GPT-like experience.

---

## 🛠️ Tech Stack

* **LLM:** Google Gemini 1.5 Flash (via `google-generativeai`)
* **Vector Store:** ChromaDB (Persistent local storage)
* **Frontend:** Streamlit
* **PDF Processing:** PyPDF
* **Language:** Python 3.9+

---

## ⚙️ Setup & Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/ntjrrvarma/vector-vault.git](https://github.com/ntjrrvarma/vector-vault.git)
    cd vector-vault
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *(Dependencies: `streamlit`, `google-generativeai`, `chromadb`, `python-dotenv`, `pypdf`)*

3.  **Configure Environment**
    Create a `.env` file in the root directory and add your Google API key:
    ```ini
    GEMINI_API_KEY=your_actual_api_key_here
    ```

---

## 🏃‍♂️ How to Run

1.  **Launch the Application**
    ```bash
    python -m streamlit run ui.py
    ```

2.  **Using the Tool**
    * Open the browser link (usually `http://localhost:8501`).
    * **Sidebar:** Upload a `.py` file (e.g., `app.py`) or a `.pdf` (e.g., `Architecture.pdf`).
    * Click **"Memorize"** to generate vector embeddings.
    * **Chat:** Ask questions like *"How does the Redis lock implementation work?"* or *"Summarize the architecture from the PDF."*

---

## 📂 Project Structure

```text
vector-vault/
├── ui.py               # Main Frontend Application (Streamlit)
├── brain.py            # Core RAG Logic (Embeddings & Retrieval)
├── chroma_db/          # Local Vector Database storage
├── .env                # API Keys (GitIgnored)
└── requirements.txt    # Python Dependencies

