import json
import os
from datetime import datetime
import ollama
from langchain_groq import ChatGroq

GROQ_API_KEY = "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"

groq_llm_mixtral = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="mixtral-8x7b-32768", temperature=0.9)
groq_llm_llama = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama3-8b-8192", temperature=0.9)

def generate_punchlines(premise, setup, comedy_type, model_info):
    prompt = f"""
You are a professional stand-up comedy writer who specializes in "{comedy_type}" comedy.

Your task is to write 3 punchlines for the setup below — each from a **different point of view** (POV), but all within the **same comedic style**: "{comedy_type}".

**Premise:** {premise}  
**Setup:** {setup}

Instructions:
- Each punchline should reflect a different character’s perspective, such as:
    - The speaker (first-person)
    - A parent, friend, stranger, pet, boss, ghost, society, etc.
- All punchlines should match the tone/style of "{comedy_type}" (e.g., dry, dark, sarcastic, etc.)
- Keep each punchline short and stage-ready (1–2 sentences max)
- Make sure the punchlines are **distinct** and not just variations of the same idea

Format your response like this:
1. [Punchline from POV #1]
2. [Punchline from POV #2]
3. [Punchline from POV #3]

Return only the punchlines. No extra explanation.
"""

    try:
        if model_info["provider"] == "groq":
            llm = groq_llm_mixtral if model_info["model"] == "mixtral-8x7b-32768" else groq_llm_llama
            stream = llm.stream([{"role": "user", "content": prompt}])
            content = "".join(chunk.content for chunk in stream)
        else:
            result = ollama.chat(
                model=model_info["model"],
                messages=[{"role": "user", "content": prompt}]
            )
            content = result["message"]["content"]

        lines = [line.strip() for line in content.split("\n") if line.strip()]
        punchlines = []
        for line in lines:
            if line[0].isdigit() and "." in line:
                _, punch = line.split(".", 1)
                punchlines.append(punch.strip())

        return punchlines[:3]

    except Exception as e:
        return [f"Error: {str(e)}"]

def save_submission(comedy_type, premise, setup, user_punchline, ai_punchlines, file_path="data/submissions.json"):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": comedy_type,
        "premise": premise,
        "setup": setup,
        "user_punchline": user_punchline,
        "ai_punchlines": ai_punchlines
    }
    os.makedirs("data", exist_ok=True)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
