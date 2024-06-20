import os
from dotenv import find_dotenv, load_dotenv
import streamlit as st
from typing import Generator
from groq import Groq

# Load environment variables from .env file
_ = load_dotenv(find_dotenv())

# Set page configuration
st.set_page_config(page_icon="🤖", layout="wide", page_title="AI Chat Bot")

# Page title and description
st.title("Groq Chat Bot with Multiple Language Models")
st.markdown("""
    Welcome to the Groq Chat Bot with Multiple Language Models. Select a model and interact with the chatbot!
""")

# Create a Groq client object
client = Groq(api_key=os.environ['GROQ_API_KEY'])

# Initialize chat history and selected model
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

# Define model details
models = {
    "llama3-70b-8192": {"name": "LLaMA3-70b", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8b", "tokens": 8192, "developer": "Meta"},
    "llama2-70b-4096": {"name": "LLaMA2-70b-chat", "tokens": 4096, "developer": "Meta"},
    "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 8192, "developer": "Google"},
    "mixtral-8x7b-32768": {
        "name": "Mixtral-8x7b-Instruct-v0.1",
        "tokens": 32768,
        "developer": "Mistral",
    },
}

# Sidebar for model selection and max_tokens slider
st.sidebar.header("Model Configuration")
model_option = st.sidebar.selectbox(
    "Choose a model:",
    options=list(models.keys()),
    format_func=lambda x: models[x]["name"],
    index=0,
)

max_tokens_range = models[model_option]["tokens"]
max_tokens = st.sidebar.slider(
    "Max Tokens:",
    min_value=512,
    max_value=max_tokens_range,
    value=min(32768, max_tokens_range),
    step=512,
    help=f"Adjust the maximum number of tokens (words) for the model's response. Max for selected model: {max_tokens_range}",
)

# Detect model change and clear chat history if model has changed
if st.session_state.selected_model != model_option:
    st.session_state.messages = []
    st.session_state.selected_model = model_option

# Add a "Clear Chat" button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = "🔋" if message["role"] == "assistant" else "🧑‍💻"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

if prompt := st.chat_input("Enter your prompt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    # Fetch response from Groq API
    try:
        chat_completion = client.chat.completions.create(
            model=model_option,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            max_tokens=max_tokens,
            stream=True,
        )

        # Use the generator function to collect responses
        response_chunks = []
        with st.chat_message("assistant", avatar="🔋"):
            for chunk in generate_chat_responses(chat_completion):
                response_chunks.append(chunk)
            full_response = ''.join(response_chunks)
            st.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        st.error(e, icon="❌")
        full_response = "Error: " + str(e)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Add footer
st.markdown("---")
st.markdown("""
**Note:** This is a demo application showcasing the capabilities of various AI models.
Developed by [Your Name](https://your-website.com).
""")
