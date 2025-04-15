# main.py
import streamlit as st
from prompts import generate_premise_and_setup
from helper import generate_punchlines, save_submission

st.set_page_config(page_title="Comedy Coach 🎤", layout="centered")

st.title("🎭 Comedyyy Coach")
st.subheader("Write punchlines. Learn by laughing.")

comedy_types = [
    "Observational", "Dark", "Self-deprecating", "Sarcastic", "Absurd/Surreal",
    "Satire", "Deadpan", "Anecdotal", "One-liner", "Parody"
]

model_options = {
    "GROQ (Gemma2 9B IT)": {"provider": "groq", "model": "gemma2-9b-it"},
    "GROQ (LLaMA3)": {"provider": "groq", "model": "llama3-8b-8192"},
    "GROQ (deepseek)": {"provider": "groq", "model": "deepseek-r1-distill-llama-70b"}
}

selected_model = st.selectbox("Choose your model:", list(model_options.keys()))
model_info = model_options[selected_model]

comedy_type = st.selectbox("Choose a type of comedy:", comedy_types)

if "GROQ_API_KEY" not in st.secrets:
    st.error("Missing GROQ_API_KEY in Streamlit secrets. Please set it in Settings → Secrets.")
    st.stop()

if st.button("Get Setup"):
    setup = generate_premise_and_setup(comedy_type, model_info)
    st.session_state["setup"] = setup
    st.session_state["model_info"] = model_info

if "setup" in st.session_state:
    
    st.markdown(f"**Setup:** {st.session_state['setup']}")

    user_punchline = st.text_input("Your punchline:")

    if st.button("See 3 sample punchlines"):
        ai_punchlines = generate_punchlines(
            st.session_state["setup"],
            comedy_type,
            st.session_state["model_info"]
        )
        for i, line in enumerate(ai_punchlines, 1):
            st.write(f"**Punchline {i}:** {line}")

        st.session_state["ai_punchlines"] = ai_punchlines

    if "ai_punchlines" in st.session_state and st.button("Save This Joke"):
        save_submission(
            comedy_type,
            st.session_state["premise"],
            st.session_state["setup"],
            user_punchline,
            st.session_state["ai_punchlines"]
        )
        st.success("Saved successfully! 🎉")
