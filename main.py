import threading
import time

from logger.activity_tracker import start_tracking

def run_tracker():
    try:
        print("Starting activity tracker...")
        start_tracking(poll_interval=5)
    except KeyboardInterrupt:
        print("Tracker stopped by user.")

if __name__ == "__main__":
    tracker_thread = threading.Thread(target=run_tracker, daemon=True)
    tracker_thread.start()

    print("Activity tracker is running in the background.")
    print("Press Ctrl+C to exit.")

    try:
        while True:
            time.sleep(1)  # Keeps the main thread alive
    except KeyboardInterrupt:
        print("Exiting loggerWorks.")
