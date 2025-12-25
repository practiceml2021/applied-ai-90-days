import os
import time
from state_manager import load_state, save_state
from logger import log_action
from cost_tracker import record_cost

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

                if "email" in file.lower():
                        action = "would send email"
                        print("📧 Action: would send email")
                else:
                        action = "logged for manual review"
                        print("🗂 Action: logged for manual review")

                record_cost("automation_agent", 0.0001)

                
                log_action(f"{file} -> {action}")
                seen.add(file)



        state["processed_files"] = list(seen)
        save_state(state)

        time.sleep(10)
