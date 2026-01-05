import os
import json
import asyncio
import time

QUEUE_DIR = "queue"
STATE_DIR = "state"

os.makedirs(STATE_DIR, exist_ok=True)

async def process_task(task):
    print(f"⚙️ Processing {task['id']}")
    await asyncio.sleep(5)
    print(f"✅ Finished {task['id']}")

def load_tasks():
    tasks = []
    for file in os.listdir(QUEUE_DIR):
        if file.endswith(".json"):
            path = os.path.join(QUEUE_DIR, file)
            with open(path, "r") as f:
                tasks.append((path, json.load(f)))
    return tasks

STALE_SECONDS = 10  # keep low for testing

def is_stale(task):
    started = task.get("started_at")
    if not started:
        return False
    return (time.time() - started) > STALE_SECONDS

async def worker_loop():
    while True:
        tasks = load_tasks()

        # recover stale in-progress tasks
        for path, task in tasks:
            if task.get("status") == "in_progress" and is_stale(task):
                print(f"♻️ Recovering stale task {task['id']}")
                task["status"] = "pending"
                task.pop("started_at", None)
                with open(path, "w") as f:
                    json.dump(task, f, indent=2)

        pending_tasks = [
            (path, task) for path, task in tasks
            if task.get("status") == "pending"
        ]

        if pending_tasks:
            path, task = pending_tasks[0]

            # mark in progress
            task["status"] = "in_progress"
            task["started_at"] = int(time.time())

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
