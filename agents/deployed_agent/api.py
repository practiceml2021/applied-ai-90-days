from fastapi import FastAPI
import asyncio
import os
import time
import json
from worker import process_task, load_tasks  # reuse your queue agent
from datetime import datetime

COST_FILE = "state/costs.json"
os.makedirs("state", exist_ok=True)

app = FastAPI()
QUEUE_DIR = "queue"

@app.post("/run")
async def run_task(payload: dict):
    task_id = f"task_{int(time.time())}"
    task = {
        "id": task_id,
        "payload": payload.get("task"),
        "status": "pending",
        "created_at": datetime.utcnow().isoformat()
    }

    os.makedirs(QUEUE_DIR, exist_ok=True)
    path = os.path.join(QUEUE_DIR, f"{task_id}.json")

    with open(path, "w") as f:
        json.dump(task, f, indent=2)

    try:
        task["status"] = "in_progress"
        with open(path, "w") as f:
            json.dump(task, f, indent=2)

        await process_task(task)

        task["status"] = "done"

    except Exception as e:
        task["status"] = "failed"
        task["error"] = str(e)

    finally:
        task["completed_at"] = datetime.utcnow().isoformat()
        with open(path, "w") as f:
            json.dump(task, f, indent=2)

    if os.path.exists(COST_FILE):
        with open(COST_FILE, "r") as f:
            cost_data = json.load(f)
    else:
        cost_data = {"total_requests": 0}

    cost_data["total_requests"] += 1

    with open(COST_FILE, "w") as f:
        json.dump(cost_data, f, indent=2)

    return {
        "id": task["id"],
        "status": task["status"],
        "error": task.get("error")
    }