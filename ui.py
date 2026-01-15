import streamlit as st
import os
from brain import add_code_to_memory, ask_brain, extract_text_from_pdf

# 1. Setup the Page
st.set_page_config(page_title="VectorVault AI", page_icon="🤖")
st.title("🤖 VectorVault: Chat with your Code")

# 2. Sidebar for Configuration
with st.sidebar:
    st.header("📂 Knowledge Loader")
    # 1. Allow PDF and Python files
    uploaded_file = st.file_uploader("Upload a file (Python or PDF)", type=["py", "pdf"])
    
    if uploaded_file:
        # Save file temporarily
        file_path = f"temp_{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 2. Check file type and Extract Text
        code_content = ""
        if uploaded_file.name.endswith(".pdf"):
            st.info("📄 PDF Detected. Extracting text...")
            code_content = extract_text_from_pdf(file_path)
        else:
            with open(file_path, "r") as f:
                code_content = f.read()
        
        # 3. Memorize
        if st.button("🧠 Memorize Data"):
            with st.spinner("Embedding into Vector Database..."):
                add_code_to_memory(uploaded_file.name, code_content)
            st.success(f"Memorized {uploaded_file.name}!")
            
            # Show preview
            with st.expander("View Extracted Content"):
                st.text(code_content[:2000] + "...") # Show first 2000 chars

# 3. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle User Input
if prompt := st.chat_input("Ask a question about your code..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = ask_brain(prompt)
                st.markdown(response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")