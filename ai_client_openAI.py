#ai_client_openAI.py

from openai import OpenAI
from ai_config import DEEPSEEK_API_KEY


client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

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

def ask_ai(history: list[dict], model: str = "deepseek-chat") -> str:

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
        {"role": m["role"], "content": m["content"]}
        for m in history
        if m.get("role") in ("user", "assistant") and m.get("content")
    ]

    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.4,
    )
    return resp.choices[0].message.content.strip()
