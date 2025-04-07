import ollama

def generate_premise_and_setup(comedy_type: str):
    prompt =  f"""
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

    response = ollama.chat(
        model="gemma3:4b",  # e.g. "llama3" or your custom model
        messages=[{"role": "user", "content": prompt}]
    )
    
    lines = response["message"]["content"].strip().split("\n")
    premise = setup = ""
    for line in lines:
        if line.lower().startswith("premise:"):
            premise = line.split(":", 1)[1].strip()
        elif line.lower().startswith("setup:"):
            setup = line.split(":", 1)[1].strip()
    return premise, setup
