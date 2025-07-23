import streamlit as st
import requests

# Load Hugging Face API key from Streamlit Cloud secret
HF_API_KEY = st.secrets["HF_API_KEY"]
API_URL = "https://api.dify.ai/v1/chat-messages"

# ✅ Verified working models
HF_MODELS = {
    "Zephy": "HuggingFaceTB/SmolLM3-3B",
    "openai": "openai/whisper-large-v3",
    "TinyLLaMA": "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
}

# Page setup
st.set_page_config(page_title="🤖 Hugging Face Chatbot", layout="centered")
st.title("🤖 Hugging Face Chatbot")

# Model selector
selected_label = st.selectbox("🧠 Choose a Model", list(HF_MODELS.keys()))
selected_model = HF_MODELS[selected_label]

# Chat history storage
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Send user message to Hugging Face
def ask_huggingface(model_id, message):
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }
    payload = {
        "inputs": message,
        "options": {"wait_for_model": True}
    }
    response = requests.post(f"{API_URL}/{model_id}", headers=headers, json=payload)
    if response.status_code == 200:
        try:
            output = response.json()
            if isinstance(output, list) and "generated_text" in output[0]:
                return output[0]["generated_text"]
            elif isinstance(output, dict) and "generated_text" in output:
                return output["generated_text"]
            elif isinstance(output, list) and "output" in output[0]:
                return output[0]["output"]
            else:
                return str(output)
        except Exception as e:
            return f"❌ Error parsing response: {e}"
    else:
        return f"❌ API error {response.status_code}: {response.text}"

# Text input
user_input = st.text_input("💬 Ask the chatbot something:")

# Generate response
if user_input:
    st.session_state.chat_history.append(("You", user_input))
    with st.spinner("Generating response..."):
        response = ask_huggingface(selected_model, user_input)
    st.session_state.chat_history.append((selected_label, response))

# Display chat
for sender, msg in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {msg}")
