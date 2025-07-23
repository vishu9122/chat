import streamlit as st
import requests

# Load secret API key from Streamlit Cloud secrets
HF_API_KEY = st.secrets["HF_API_KEY"]
API_URL_BASE = "https://api-inference.huggingface.co/models"

# UI setup
st.set_page_config(page_title="Hugging Face Chatbot", layout="centered")
st.title("🤖 Hugging Face Chatbot")

HF_MODELS = {
    "LLaMA 2 (7B)": "meta-llama/Llama-2-7b-chat-hf",
    "Mixtral 8x7B": "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "Falcon RW 1B": "tiiuae/falcon-rw-1b",
    "Gemma 7B": "google/gemma-7b-it",
    "OpenChat 3.5": "openchat/openchat-3.5",
    "Mistral 7B Instruct": "mistralai/Mistral-7B-Instruct-v0.1"
}

# Model selection
model_name = st.selectbox("🧠 Select a model:", list(HF_MODELS.keys()))
model_id = HF_MODELS[model_name]

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("💬 Ask something:")

# Call Hugging Face API
def query_huggingface(model, prompt):
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }
    response = requests.post(f"{API_URL_BASE}/{model}", headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "")
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

# Display chat
if user_input:
    st.session_state.chat_history.append(("You", user_input))
    with st.spinner("Generating response..."):
        response = query_huggingface(model_id, user_input)
    st.session_state.chat_history.append(("Bot", response))

# Show chat history
for sender, msg in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {msg}")
