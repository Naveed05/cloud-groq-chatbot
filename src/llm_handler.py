import os
from langchain_groq import ChatGroq

def load_groq_model(model="llama3-8b", temperature=0.7):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY missing! Add it to .env")

    return ChatGroq(
        groq_api_key=api_key,
        model=model,
        temperature=temperature
    )
