import streamlit as st
import requests
import base64
from io import BytesIO

st.title("🚢 Titanic Chatbot")

query = st.text_input("Ask me about the Titanic dataset:")

if query:
    response = requests.get(f"http://127.0.0.1:8000/query?text={query}").json()

    # Handle text responses
    if "answer" in response:
        st.write(response["answer"])

    # Handle image responses (histogram)
    elif "image" in response:
        img_data = base64.b64decode(response["image"])
        st.image(BytesIO(img_data), caption="Generated Visualization")

    # Handle unexpected response format
    else:
        st.error("Unexpected response format from backend!")
