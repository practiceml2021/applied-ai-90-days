import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
API_URL = "https://api.openai.com/v1/chat/completions"

def summarize(text: str, question: str):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a research assistant.

Answer the research question using ONLY the information in the text.

Question:
{question}

Text:
{text}

Rules:
- Return 3–5 bullet points
- Each bullet must end with: "(from retrieved source)"
- If the answer cannot be found, say: "Not found in retrieved sources"
- Do not add outside knowledge
"""


    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
