from datetime import datetime

LOG_FILE = "state/actions.log"

def log_action(message: str):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - {message}\n")
