import threading
import time
import tkinter as tk

from logger.activity_tracker import start_tracking
from gui.app_window import LoggerApp

stop_tracking = False

def run_tracker():
    while not stop_tracking:
        from logger.activity_tracker import get_active_window_info
        from logger.file_logger import log_activity

        app_name, window_title = get_active_window_info()
        log_activity(f"{app_name} - {window_title}")
        time.sleep(5)

def stop_logging():
    global stop_tracking
    stop_tracking = True

if __name__ == "__main__":
    tracker_thread = threading.Thread(target=run_tracker, daemon=True)
    tracker_thread.start()

    root = tk.Tk()
    app = LoggerApp(root, stop_callback=stop_logging)
    root.mainloop()
