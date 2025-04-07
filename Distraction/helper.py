import json
import os
from datetime import datetime
import ollama

# Generate with Ollama
def generate_punchlines(premise, setup, comedy_type):
#     prompt = f"""
# You are a professional stand-up comedy writer, and your style is "{comedy_type}" comedy.

# Based on the following premise and setup, write **three different punchlines**, each taking a **different direction or comedic angle** — but all still in the tone of "{comedy_type}" comedy.

# **Premise:** {premise}  
# **Setup:** {setup}

# Requirements:
# - All 3 punchlines must match the selected comedy style: {comedy_type}
# - Each punchline should explore a **different approach**, such as:
#     - Literal or observational
#     - Sarcastic or ironic
#     - Absurd or exaggerated
#     - Wordplay or clever twist
#     - Dark interpretation (if comedy type is dark), etc.
# - Punchlines should be short (1–2 sentences max), punchy, and stage-ready.
# - Avoid repeating logic — each one should feel fresh and unique.

# Format your response like this:
# 1. First punchline
# 2. Second punchline
# 3. Third punchline

# Return only the punchlines — no extra explanation.
# """

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
        response = ollama.chat(
            model="gemma3:4b",  # e.g., "mistral", "phi", etc.
            messages=[{"role": "user", "content": prompt}]
        )

        content = response['message']['content'].strip()
        lines = [line.strip() for line in content.split("\n") if line.strip()]
        
        # Clean up and only keep numbered lines
        punchlines = []
        for line in lines:
            if line[0].isdigit() and "." in line:
                _, punch = line.split(".", 1)
                punchlines.append(punch.strip())

        return punchlines[:3]  # Return max 3 clean lines

    except Exception as e:
        return [f"Error generating punchlines: {str(e)}"]

# Save to JSON
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
