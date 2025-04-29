import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import os

from logger.disable_logger import log_disable_event

class LoggerApp:
    def __init__(self, root, stop_callback):
        self.root = root
        self.stop_callback = stop_callback

        self.root.title("loggerWorks")
        self.root.geometry("600x400")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.button = tk.Button(root, text="Disable Logging", command=self.disable_logging, bg="red", fg="white")
        self.button.pack(pady=5)

        self.load_today_log()

    def load_today_log(self):
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = f"logs/{today}.txt"

        self.text_area.delete(1.0, tk.END)

        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                self.text_area.insert(tk.END, f.read())
        else:
            self.text_area.insert(tk.END, "No log entries for today.")

    def disable_logging(self):
        log_disable_event()
        self.stop_callback()
        self.button.config(text="Logging Disabled", state=tk.DISABLED)
