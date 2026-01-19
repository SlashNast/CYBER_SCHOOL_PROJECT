#ai_client
from openai import OpenAI
from config import DEEPSEEK_API_KEY
import threading

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

SYSTEM_PROMPT = (
    "Ты — учитель математики для 7–9 классов."
    "Объясняй шагами, простым языком."
    "Если ученик просит подсказку — дай 1 шаг, без финального ответа."
    "Если просит полное решение — дай решение и проверку."
    "Если данных не хватает — задай 1 уточняющий вопрос."
    "Язык ответа: как у пользователя (RU/HE/EN)."

)

def ask_ai(history: list[dict], model: str = "deepseek-chat") -> str:
    # DeepSeek API: chat completions style :contentReference[oaicite:2]{index=2}
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
