import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="RAG for Academic Articles",
    page_icon="📚"
)

st.title("📚 RAG Assistant for Academic Articles")
st.caption("Ask a question about the documents you have processed.")

# --- Backend API URL ---
API_URL = "http://127.0.0.1:8000/generate-response/"

# --- User Input ---
question = st.text_input(
    "Enter your question here:",
    key="question_input"
)

# --- Ask Button and Response Logic ---
if st.button("Ask", key="ask_button"):
    if question:
        # Show a spinner while processing
        with st.spinner("Retrieving context and generating answer..."):
            try:
                # Data to send to the API
                payload = {"question": question}

                # Send POST request to the FastAPI backend [cite: 107]
                response = requests.post(API_URL, json=payload, timeout=300) # [cite: 110, 111, 112]

                if response.status_code == 200:
                    api_response = response.json()
                    st.success("Here is the answer:")
                    st.write(api_response.get("response", "No response content found."))
                else:
                    st.error(f"Error: Received status code {response.status_code}")
                    st.json(response.json())

            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to the backend API: {e}")
    else:
        st.warning("Please enter a question.")