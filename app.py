from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from src.chat_engine import generate_response
import time

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(
    page_title="Groq ChatGPT-Style Chatbot",
    layout="centered"
)

st.title("🤖 Cloud Chatbot (Groq API)")
st.write("Ultra-fast ChatGPT-like responses powered by Groq LLaMA, Qwen, and GPT-OSS models.")

# ----------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------
st.sidebar.header("⚙️ Model Settings")

# VALID GROQ FREE-TIER MODELS
selected_model = st.sidebar.selectbox(
    "Choose Model",
    [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "qwen/qwen3-32b",
        "gpt-oss-20b",
        "gpt-oss-120b"
    ]
)

temperature = st.sidebar.slider(
    "Temperature (Creativity)",
    0.0, 1.5, 0.7
)

system_prompt = st.sidebar.text_area(
    "System Prompt (Bot Personality)",
    value=(
        "You are a highly intelligent, friendly AI assistant. "
        "You answer ANY question naturally like ChatGPT."
    )
)

if st.sidebar.button("Clear Chat 🔄"):
    st.session_state.chat = []
    st.session_state.last_input = None

# ----------------------------------------------------------
# INIT CHAT
# ----------------------------------------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

if "last_input" not in st.session_state:
    st.session_state.last_input = None

# ----------------------------------------------------------
# DISPLAY CHAT HISTORY
# ----------------------------------------------------------
for role, message in st.session_state.chat:
    if role == "user":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Assistant:** {message}")

# ----------------------------------------------------------
# INPUT FIELD
# ----------------------------------------------------------
user_input = st.text_input("Your message:", key="input_box")

# ----------------------------------------------------------
# PROCESS INPUT
# ----------------------------------------------------------
if user_input and st.session_state.last_input != user_input:

    st.session_state.last_input = user_input
    st.session_state.chat.append(("user", user_input))

    typing_ph = st.empty()
    typing_ph.markdown("🤖 *Assistant is typing...*")

    try:
        response = generate_response(
            question=user_input,
            model=selected_model,
            temp=temperature,
            system_prompt=system_prompt
        )

        # Typewriter effect
        text = ""
        for ch in response:
            text += ch
            typing_ph.markdown(f"**🤖 Assistant:** {text}")
            time.sleep(0.01)

        typing_ph.empty()
        st.session_state.chat.append(("assistant", response))

    except Exception as e:
        typing_ph.markdown(f"❌ Error: {str(e)}")

# ----------------------------------------------------------
# CLEAR BUTTON IN MAIN PAGE
# ----------------------------------------------------------
if st.button("Clear Chat"):
    st.session_state.chat = []
    st.session_state.last_input = None
    st.rerun()
