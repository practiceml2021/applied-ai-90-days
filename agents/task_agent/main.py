import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime
from pydantic import BaseModel, ValidationError
from typing import List

class TaskPlan(BaseModel):
    steps: List[str]


load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
API_URL = "https://api.openai.com/v1/responses"


def get_task_breakdown(goal: str) -> dict:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a planning assistant.

You MUST respond with ONLY valid JSON.
DO NOT include explanations, markdown, or extra text.

Required format:
{{
  "steps": [
    "Step 1",
    "Step 2",
    "Step 3"
  ]
}}

Goal: {goal}
"""

    payload = {
        "model": "gpt-4.1-mini",
        "input": prompt,
        "temperature": 0.0
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=30
    )
    response.raise_for_status()

    data = response.json()
    text = data["output"][0]["content"][0]["text"]

    # 🔒 HARD JSON EXTRACTION
    start = text.find("{")
    end = text.rfind("}") + 1

    if start == -1 or end == -1:
        raise RuntimeError("No JSON object found in model output")

    json_text = text[start:end]

    parsed = json.loads(json_text)

    if not isinstance(parsed, dict):
        raise RuntimeError("Parsed output is not a dict")

    return parsed



def save_tasks_to_file(task_data: dict):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"tasks_{timestamp}.json"

    try:
        validated = TaskPlan(**task_data)
    except ValidationError as ve:
        print("❌ Output does not match expected schema.")
        print(ve)
        return

    with open(filename, "w") as f:
        json.dump(validated.dict(), f, indent=2)

    print(f"✅ Validated tasks saved to {filename}")



if __name__ == "__main__":
    goal = input("Enter your goal: ")

    try:
        result = get_task_breakdown(goal)

        print("\n--- Parsed Output ---")
        print(json.dumps(result, indent=2))

        save_tasks_to_file(result)

    except Exception as e:
        print("❌ Error occurred:", str(e))

