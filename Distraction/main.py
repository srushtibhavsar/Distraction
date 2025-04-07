import streamlit as st
from prompts import generate_premise_and_setup
from helper import generate_punchlines, save_submission

st.set_page_config(page_title="Comedy Coach 🎤", layout="centered")

st.title("🎭 Comedy Coach")
st.subheader("Write punchlines. Learn by laughing.")

comedy_types = [
    "Observational",         # Everyday life and relatable things
    "Dark",                  # Morbid, edgy, taboo topics with humor
    "Self-deprecating",      # Making fun of yourself
    "Sarcastic",             # Ironic, biting humor
    "Absurd/Surreal",        # Nonsense, bizarre logic, dream-like humor
    "Satire",                # Critiquing politics, society, or culture
    "Deadpan",               # Emotionless delivery of wild punchlines
    "Anecdotal",             # Story-based humor from life events
    "One-liner",             # Short, sharp jokes with punchy lines
    "Parody",                # Making fun of genres, people, pop culture
]


# 1. Select comedy type
comedy_type = st.selectbox("Choose a type of comedy:", comedy_types)

# 2. Generate premise + setup
if st.button("Get Premise & Setup"):
    premise, setup = generate_premise_and_setup(comedy_type)
    st.session_state["premise"] = premise
    st.session_state["setup"] = setup

# Show current setup
if "setup" in st.session_state:
    st.markdown(f"**Premise:** {st.session_state['premise']}")
    st.markdown(f"**Setup:** {st.session_state['setup']}")

    # 3. User writes punchline
    user_punchline = st.text_input("Your punchline:")

    # 4. Show AI-generated punchlines
    if st.button("See 3 sample punchlines"):
        ai_punchlines = generate_punchlines(st.session_state["premise"], st.session_state["setup"], comedy_type)
        for i, line in enumerate(ai_punchlines, 1):
            st.write(f"**Punchline {i}:** {line}")

        # 5. Save submission
        save_submission(comedy_type, st.session_state["premise"], st.session_state["setup"], user_punchline, ai_punchlines)
