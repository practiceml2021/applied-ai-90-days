import os
import time
from state_manager import load_state, save_state

TASKS_DIR = "../task_agent"

def find_task_files():
    return [
        f for f in os.listdir(TASKS_DIR)
        if f.startswith("tasks_") and f.endswith(".json")
    ]

if __name__ == "__main__":
    state = load_state()
    seen = set(state.get("processed_files", []))

    print("🔁 Automation agent started")

    while True:
        files = find_task_files()

        for file in files:
            if file not in seen:
                print(f"🆕 New task file detected: {file}")
                seen.add(file)

        state["processed_files"] = list(seen)
        save_state(state)

        time.sleep(10)
