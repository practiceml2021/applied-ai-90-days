import os
import json
import asyncio
from time import sleep

QUEUE_DIR = "queue"
STATE_DIR = "state"

os.makedirs(STATE_DIR, exist_ok=True)

async def process_task(task):
    print(f"⚙️ Processing {task['id']}")
    await asyncio.sleep(5)  # simulate long work
    print(f"✅ Finished {task['id']}")

def load_tasks():
    tasks = []
    for file in os.listdir(QUEUE_DIR):
        if file.endswith(".json"):
            path = os.path.join(QUEUE_DIR, file)
            with open(path, "r") as f:
                tasks.append((path, json.load(f)))
    return tasks

async def worker_loop():
    while True:
        tasks = load_tasks()

        for path, task in tasks:
            if task.get("status") != "pending":
                continue

            # mark in-progress
            task["status"] = "in_progress"
            with open(path, "w") as f:
                json.dump(task, f, indent=2)

            await process_task(task)

            # mark done
            task["status"] = "done"
            with open(path, "w") as f:
                json.dump(task, f, indent=2)

        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(worker_loop())
