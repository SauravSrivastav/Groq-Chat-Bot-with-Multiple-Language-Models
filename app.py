import os
import streamlit as st
from typing import Generator
from groq import Groq
import json
from datetime import datetime

# Set page configuration
st.set_page_config(page_icon="🤖", layout="wide", page_title="Groq Chat Bot")

# Custom theme
st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .chat-message.user {
        background-color: #2b313e;
    }
    .chat-message.bot {
        background-color: #475063;
    }
    .chat-message .avatar {
        width: 20%;
    }
    .chat-message .content {
        width: 80%;
    }
    .chat-message .content p {
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Page title and description
st.title("Groq Chat Bot with Multiple Language Models")
st.markdown("""
    Welcome to the Groq Chat Bot with Multiple Language Models. Select a model and interact with the chatbot!
""")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_model" not in st.session_state:
    st.session_state.selected_model = None
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Define model details
models = {
    "llama3-70b-8192": {"name": "LLaMA3-70b", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8b", "tokens": 8192, "developer": "Meta"},
    "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 8192, "developer": "Google"},
    "mixtral-8x7b-32768": {
        "name": "Mixtral-8x7b-Instruct-v0.1",
        "tokens": 32768,
        "developer": "Mistral",
    },
}

# Sidebar for configuration
st.sidebar.header("Configuration")

# API Key input
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")
if api_key:
    st.session_state.api_key = api_key

# Model selection
model_option = st.sidebar.selectbox(
    "Choose a model:",
    options=list(models.keys()),
    format_func=lambda x: models[x]["name"],
    index=0,
)

# Display model information
st.sidebar.markdown(f"""
**Model Information:**
- Name: {models[model_option]['name']}
- Max Tokens: {models[model_option]['tokens']}
- Developer: {models[model_option]['developer']}
""")

# Max tokens slider
max_tokens_range = models[model_option]["tokens"]
max_tokens = st.sidebar.slider(
    "Max Tokens:",
    min_value=512,
    max_value=max_tokens_range,
    value=min(4096, max_tokens_range),
    step=512,
    help=f"Adjust the maximum number of tokens for the model's response. Max: {max_tokens_range}",
)

# Temperature slider
temperature = st.sidebar.slider(
    "Temperature:",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
    help="Adjust the randomness of the model's responses. Higher values make output more random.",
)

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

# Export chat button
if st.sidebar.button("Export Chat"):
    chat_export = {
        "model": model_option,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messages": st.session_state.messages
    }
    st.sidebar.download_button(
        label="Download Chat History",
        data=json.dumps(chat_export, indent=2),
        file_name="chat_export.json",
        mime="application/json"
    )

# Detect model change and clear chat history if model has changed
if st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# Chat input
if prompt := st.chat_input("Enter your prompt here..."):
    if not st.session_state.api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        # Create Groq client
        client = Groq(api_key=st.session_state.api_key)

        # Fetch response from Groq API
        try:
            chat_completion = client.chat.completions.create(
                model=model_option,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True,
            )

            # Use the generator function to collect responses
            response_chunks = []
            with st.chat_message("assistant", avatar="🤖"):
                message_placeholder = st.empty()
                for chunk in generate_chat_responses(chat_completion):
                    response_chunks.append(chunk)
                    message_placeholder.markdown(''.join(response_chunks) + "▌")
                full_response = ''.join(response_chunks)
                message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"An error occurred: {str(e)}", icon="❌")

# Add footer
st.markdown("---")
st.markdown("""
**Note:** This is a demo application showcasing the capabilities of various AI models.
Developed by [Your Name](https://your-website.com).
""")
