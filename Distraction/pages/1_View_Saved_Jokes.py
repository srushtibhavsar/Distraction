# pages/1_View_Saved_Jokes.py
import streamlit as st
import json
import os

st.set_page_config(page_title="Saved Jokes", layout="centered")
st.title("📘 Saved Jokes")

file_path = "data/submissions.json"

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    for entry in reversed(data):
        with st.expander(f"{entry['timestamp']} - {entry['type']} Comedy"):
            st.markdown(f"**Setup:** {entry['setup']}")
            st.markdown(f"**User Punchline:** {entry['user_punchline']}")
            st.markdown("**AI Punchlines:**")
            for i, punch in enumerate(entry["ai_punchlines"], 1):
                st.markdown(f"- {punch}")
else:
    st.info("No saved jokes yet. Try generating and saving some first!")
