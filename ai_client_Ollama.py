#ai_client_Ollama.py

import requests

SYSTEM_PROMPT = (
    "You are an assistant for 11th–12th grade students in Israeli schools."
"You should help students when they have questions or difficulties solving Bagrut exams."
"You will help with subjects such as mathematics, English, and physics."
"Explain step by step, using simple language."
"If a student asks for a hint — give only one step, without the final answer."
"If the student asks for a full solution — provide the full solution and verification."
"If the student asks to explain a topic, always include several examples together with the explanation."
"At the end of each explanation, suggest practicing with simple examples that you create yourself."
"If there is not enough information — ask clarifying questions."
"Respond in the same language as the user (RU/HE/EN)."

"At the end of every response, add a cat emoji."
)

def ask_ai(history: list[dict], model: str = "llama3.1") -> str:

    text = SYSTEM_PROMPT + "\n\n"
    for m in history:
        if m["role"] == "user":
            text += f"USER: {m['content']}\n"
        elif m["role"] == "assistant":
            text += f"ASSISTANT: {m['content']}\n"

    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": text, "stream": False},
        timeout=120
    )
    r.raise_for_status()
    return r.json()["response"].strip()
