from datetime import datetime
import os

DISABLE_LOG_FILE = "logs/disable_log.txt"
os.makedirs("logs", exist_ok=True)

def log_disable_event():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(DISABLE_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"Logging disabled at: {now}\n")
