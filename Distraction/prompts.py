# prompts.py
import streamlit as st
import ollama
from langchain_groq import ChatGroq

def get_groq_llm(model_name: str, temperature: float = 0.8):
    return ChatGroq(
        groq_api_key=st.secrets["GROQ_API_KEY"],
        model_name=model_name,
        temperature=temperature
    )

def generate_premise_and_setup(comedy_type: str, model_info: dict):
    prompt = f"""
You are an expert stand-up comedy writer known for {comedy_type.lower()} humor.

Create one original joke **premise** and **setup** in this comedy style.

- The **premise** should introduce the theme or idea of the joke (1 sentence).
- The **setup** should build tension or curiosity without being the punchline (1 sentence).
- Make sure the setup leads naturally to a potential punchline.
- Keep it short, sharp, and clever — like real stand-up material.

Output format:
Premise: <your premise>
Setup: <your setup>
"""

    if model_info["provider"] == "groq":
        llm = get_groq_llm(model_info["model"])
        stream = llm.stream([{"role": "user", "content": prompt}])
        content = "".join(chunk.content for chunk in stream)
    else:
        response = ollama.chat(
            model=model_info["model"],
            messages=[{"role": "user", "content": prompt}]
        )
        content = response["message"]["content"]

    lines = content.strip().split("\n")
    premise = setup = ""
    for line in lines:
        if line.lower().startswith("premise:"):
            premise = line.split(":", 1)[1].strip()
        elif line.lower().startswith("setup:"):
            setup = line.split(":", 1)[1].strip()
    return premise, setup