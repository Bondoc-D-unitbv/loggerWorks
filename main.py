import threading
import time
import tkinter as tk

from logger.activity_tracker import get_active_window_info
from logger.file_logger import log_activity
from gui.app_window import LoggerApp

tracking_active = True

def run_tracker():
    while True:
        if tracking_active:
            app_name, window_title = get_active_window_info()
            log_activity(f"{app_name} - {window_title}")
        time.sleep(5)

def toggle_tracking(new_state):
    global tracking_active
    tracking_active = new_state

if __name__ == "__main__":
    tracker_thread = threading.Thread(target=run_tracker, daemon=True)
    tracker_thread.start()

    root = tk.Tk()
    app = LoggerApp(root, toggle_callback=toggle_tracking, is_tracking_active=tracking_active)
    root.mainloop()
