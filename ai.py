import requests


def ask_ai(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


def split_text(text, size=3000):

    parts = []

    for i in range(0, len(text), size):
        parts.append(text[i:i+size])

    return parts