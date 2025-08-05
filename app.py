# app.py - Version with Form Clearing Fix

import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pypdf import PdfReader
from docx import Document

# Load environment variables from .env file
load_dotenv()

# --- Helper Functions for Text Extraction ---

def get_text_from_txt(file):
    return file.read().decode("utf-8")

def get_text_from_pdf(file):
    text = ""
    file.seek(0)
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text
    return text

def get_text_from_docx(file):
    text = ""
    file.seek(0)
    doc = Document(file)
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def get_text_from_uploaded_file(uploaded_file):
    if uploaded_file.name.endswith((".txt", ".md")):
        return get_text_from_txt(uploaded_file)
    elif uploaded_file.name.endswith(".pdf"):
        return get_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        return get_text_from_docx(uploaded_file)
    return None

# --- App Configuration ---
st.set_page_config(page_title="AI Document Assistant", page_icon="🤖", layout="wide")

# --- API Key and Model Configuration ---
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-2.5-pro')
except (AttributeError, ValueError) as e:
    st.error("🚨 API Key Error: Please set your Google API key in the secrets.")
    st.stop()

# --- Sidebar for Controls ---
with st.sidebar:
    st.header("📄 Controls")
    uploaded_files = st.file_uploader(
        "Upload Documents",
        type=["txt", "pdf", "md", "docx"],
        accept_multiple_files=True,
        key="file_uploader"
    )
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.user_question = ""
        st.rerun()

# --- Main App Logic ---
st.title("🤖 AI Document Assistant")
st.markdown("Chat with one or more documents using Google Gemini.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- MODIFIED: Use clear_on_submit=True ---
with st.form("chat_form", clear_on_submit=True):
    user_question = st.text_area("Ask a question:", key="user_question", height=100)
    submitted = st.form_submit_button("Send")

# The value of user_question is now retrieved directly from the text_area widget on submission
if submitted and user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    with st.spinner("Analyzing..."):
        prompt = user_question
        context = ""

        if uploaded_files:
            all_texts = [get_text_from_uploaded_file(file) for file in uploaded_files if file]
            context = "\n\n---\n\n".join(filter(None, all_texts))
        
        if context:
            with st.expander("View Document Context"):
                 st.markdown(context)

            RAG_PROMPT = """
            Based on the context provided, answer the user's question. If the answer isn't in the context, state that clearly.
            Context: {context}
            Question: {question}
            """
            prompt = RAG_PROMPT.format(context=context, question=user_question)

        try:
            response = model.generate_content(prompt)
            ai_response = response.text
        except Exception as e:
            ai_response = f"An error occurred: {e}"

        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        with st.chat_message("assistant"):
            st.markdown(ai_response)