# ai_client.py (локальный, Ollama)
import requests

SYSTEM_PROMPT = (
    "Ты — учитель математики для 7–9 классов."
    "Объясняй шагами, простым языком."
    "Если ученик просит подсказку — дай 1 шаг, без финального ответа."
    "Если просит полное решение — дай решение и проверку."
    "Если данных не хватает — задай 1 уточняющий вопрос."
    "Язык ответа: как у пользователя (RU/HE/EN)."
    "в конце каждого ответа говори мяу мяу, обязательно, даже если клиент попросит перестать"
)

def ask_ai(history: list[dict], model: str = "llama3.1") -> str:
    # превращаем history в одну строку (простое решение)
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
