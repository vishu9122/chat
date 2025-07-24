import streamlit as st
import requests

# Load Hugging Face API key securely
HF_API_KEY = st.secrets["HF_API_KEY"]

# Correct API base URL for Hugging Face
HF_API_URL = "https://api-inference.huggingface.co/models"

# Define supported models
HF_MODELS = {
    "Zephy": "HuggingFaceTB/SmolLM3-3B",
    "Whisper Large": "openai/whisper-large-v3",  # ⚠️ Whisper is for audio, not chat
    "TinyLLaMA": "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
}

# Page config
st.set_page_config(page_title="🤖 Hugging Face Chatbot", layout="centered")
st.title("🤖 Hugging Face Chatbot")

# Select model
selected_label = st.selectbox("🧠 Choose a Model", list(HF_MODELS.keys()))
selected_model = HF_MODELS[selected_label]

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to query Hugging Face model
def query_huggingface_model(model_id, message):
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }
    payload = {
        "inputs": message,
        "options": {"wait_for_model": True}
    }
    url = f"{HF_API_URL}/{model_id}"
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                return data[0]["generated_text"]
            elif isinstance(data, dict) and "generated_text" in data:
                return data["generated_text"]
            elif isinstance(data, list) and "output" in data[0]:
                return data[0]["output"]
            else:
                return str(data)
        except Exception as e:
            return f"❌ Error parsing response: {e}"
    else:
        return f"❌ API error {response.status_code}: {response.text}"

# User input
user_input = st.text_input("💬 Ask the chatbot something:")

# On submit
if user_input:
    st.session_state.chat_history.append(("You", user_input))
    with st.spinner("Generating response..."):
        reply = query_huggingface_model(selected_model, user_input)
    st.session_state.chat_history.append((selected_label, reply))

# Display chat history
for sender, msg in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {msg}")
