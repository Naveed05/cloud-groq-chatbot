from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os


def generate_response(question, model, temp, system_prompt):
    """
    Generate an AI response using Groq selected model.
    """

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "❌ GROQ_API_KEY missing in .env"

    # Load dynamic Groq model
    llm = ChatGroq(
        api_key=api_key,
        model=model,        # <- Correct dynamic model
        temperature=temp
    )

    # Build prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", question)
    ])

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"question": question})
