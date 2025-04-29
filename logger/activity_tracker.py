import time
import win32gui # type: ignore
import win32process # type: ignore
import psutil # type: ignore

from logger.file_logger import log_activity



def get_active_window_info():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        app_name = process.name()
        window_title = win32gui.GetWindowText(hwnd)
        return app_name, window_title
    except Exception as e:
        return "Unknown", f"Error: {str(e)}"


def start_tracking(poll_interval=5):
    last_activity = None

    while True:
        app_name, window_title = get_active_window_info()
        activity = f"{app_name} - {window_title}"

        # Only log if activity changes (avoid duplicates)
        if activity != last_activity:
            log_activity(activity)
            last_activity = activity

        time.sleep(poll_interval)
