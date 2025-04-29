import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_activity(activity):
    now = datetime.now()
    filename = os.path.join(LOG_DIR, now.strftime("%Y-%m-%d") + ".txt")
    timestamp = now.strftime("%H:%M:%S")

    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {activity}\n")
