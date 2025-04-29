import tkinter as tk
from tkinter import scrolledtext
from tkcalendar import DateEntry # type: ignore
from datetime import datetime
import os

from logger.disable_logger import log_disable_event

class LoggerApp:
    def __init__(self, root, toggle_callback, is_tracking_active):
        self.root = root
        self.toggle_callback = toggle_callback
        self.is_tracking_active = is_tracking_active
        self.selected_date = datetime.now().strftime("%Y-%m-%d")

        self.root.title("loggerWorks")
        self.root.geometry("700x500")

        # === Date Picker ===
        self.date_picker = DateEntry(root, width=12, background='darkblue',
                                     foreground='white', borderwidth=2,
                                     year=datetime.now().year)
        self.date_picker.pack(pady=5)
        self.date_picker.bind("<<DateEntrySelected>>", self.on_date_selected)

        # === Load Logs Button ===
        self.load_button = tk.Button(root, text="Load Logs", command=self.load_selected_log)
        self.load_button.pack(pady=5)

        # === Log Viewer ===
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # === Toggle Logging Button ===
        self.toggle_button = tk.Button(root, text="", command=self.toggle_logging)
        self.toggle_button.pack(pady=5)

        self.update_toggle_button()
        self.load_log_for_date(self.selected_date)
        self.auto_refresh()

    def load_log_for_date(self, date):
        self.selected_date = date
        log_file = f"logs/{date}.txt"
        self.text_area.delete(1.0, tk.END)

        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                self.text_area.insert(tk.END, f.read())
        else:
            self.text_area.insert(tk.END, f"No log entries for {date}.")

    def load_selected_log(self):
        date = self.date_picker.get_date().strftime("%Y-%m-%d")
        self.load_log_for_date(date)

    def on_date_selected(self, event):
        self.load_selected_log()

    def toggle_logging(self):
        self.is_tracking_active = not self.is_tracking_active
        self.toggle_callback(self.is_tracking_active)
        if not self.is_tracking_active:
            log_disable_event()
        self.update_toggle_button()

    def update_toggle_button(self):
        if self.is_tracking_active:
            self.toggle_button.config(text="Disable Logging", bg="red", fg="white")
        else:
            self.toggle_button.config(text="Enable Logging", bg="green", fg="white")

    def auto_refresh(self):
        # Only auto-refresh if viewing today's log
        current_date = datetime.now().strftime("%Y-%m-%d")
        if self.selected_date == current_date:
            self.load_log_for_date(self.selected_date)
        self.root.after(5000, self.auto_refresh)
