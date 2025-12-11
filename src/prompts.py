from langchain_core.prompts import ChatPromptTemplate

def build_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", "You are ChatGPT-like assistant. Respond clearly, professionally, and with high accuracy."),
        ("user", "{question}")
    ])
