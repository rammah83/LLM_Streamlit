import os
import streamlit as st
import PyPDF2
import requests

# Set up the API key for Hugging Face Inference API
API_TOKEN = open("./tokens_key.secret", "r").read().strip()
if not API_TOKEN:
    st.error("Please set the HUGGINGFACE_API_TOKEN in the 'tokens_key.secret' file.")
    st.stop()

headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Update the API URL to use Llama 2
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text



st.title("Chat with your PDF using Llama 2")
# Initialize session state variables
if "pdf_text" not in st.session_state:
    st.session_state["pdf_text"] = ""
if "messages" not in st.session_state:
    st.session_state["messages"] = []
# PDF file uploader
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
if uploaded_file is not None:
    # Extract text from the PDF file
    with st.spinner("Extracting text from PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.session_state["pdf_text"] = pdf_text
    st.success("PDF text extracted and loaded.")
# Check if PDF text is available
if st.session_state["pdf_text"]:
    # Create a form to accept user input
    with st.form(key="user_input_form", clear_on_submit=True):
        user_input = st.text_input("You:")
        submit_button = st.form_submit_button(label="Send")
    if submit_button and user_input:
        # Prepare the prompt for the Llama 2 model
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based on the provided document.",
            },
            {
                "role": "user",
                "content": f"Document: {st.session_state['pdf_text']}\n\nQuestion: {user_input}",
            },
        ]
        # Query the Llama 2 model
        with st.spinner("Thinking..."):
            output = query(
                {
                    "inputs": messages,
                    "parameters": {
                        "max_new_tokens": 512,
                        "temperature": 0.7,
                        "return_full_text": False,
                    },
                    "options": {"wait_for_model": True},
                }
            )
            # Handle API errors
            if isinstance(output, dict) and output.get("error"):
                st.error(f"Error: {output['error']}")
            else:
                # Extract the generated answer
                if isinstance(output, dict) and output.get("generated_text"):
                    answer = output["generated_text"]
                else:
                    answer = "Sorry, I could not generate a response."
                # Save the conversation
                st.session_state["messages"].append(
                    {"user": user_input, "bot": answer}
                )
    # Display the conversation history
    if st.session_state.get("messages"):
        for msg in st.session_state["messages"]:
            st.markdown(f"**You:** {msg['user']}")
            st.markdown(f"**Assistant:** {msg['bot']}")
else:
    st.info("Please upload a PDF file to get started.")