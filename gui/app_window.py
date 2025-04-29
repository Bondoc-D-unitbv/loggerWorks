from tkcalendar import Calendar
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import os

class LoggerApp:
    def __init__(self, root, toggle_callback, is_tracking_active):
        self.root = root
        self.toggle_callback = toggle_callback
        self.is_tracking_active = is_tracking_active
        self.selected_date = datetime.now().strftime("%Y-%m-%d")

        self.root.title("loggerWorks")
        self.root.geometry("750x550")

        # === Calendar ===
        self.calendar = Calendar(self.root, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.pack(pady=5)
        self.calendar.bind("<<CalendarSelected>>", self.on_date_selected)

        # === Log Count Label ===
        self.log_count_label = tk.Label(self.root, text="")
        self.log_count_label.pack()

        # === Load Logs Button ===
        self.load_button = tk.Button(root, text="Load Logs", command=self.load_selected_log)
        self.load_button.pack(pady=5)

        # === Log Viewer ===
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # === Toggle Button ===
        self.toggle_button = tk.Button(root, text="", command=self.toggle_logging)
        self.toggle_button.pack(pady=5)

        self.update_toggle_button()
        self.mark_log_days()
        self.load_log_for_date(self.selected_date)
        self.auto_refresh()

    def get_log_entry_count(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return sum(1 for _ in f)
        except:
            return 0

    def mark_log_days(self):
        log_dir = "logs"
        if not os.path.exists(log_dir):
            return

        for filename in os.listdir(log_dir):
            if filename.endswith(".txt"):
                date_str = filename.replace(".txt", "")
                file_path = os.path.join(log_dir, filename)
                count = self.get_log_entry_count(file_path)

                # Color intensity based on log count
                if count > 50:
                    color = "darkblue"
                elif count > 20:
                    color = "blue"
                elif count > 0:
                    color = "lightblue"
                else:
                    continue

                try:
                    self.calendar.calevent_create(datetime.strptime(date_str, "%Y-%m-%d"), f"{count} logs", "log")
                    self.calendar.tag_config("log", background=color, foreground="white")
                except:
                    pass

    def load_log_for_date(self, date):
        self.selected_date = date
        log_file = f"logs/{date}.txt"
        self.text_area.delete(1.0, tk.END)

        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                contents = f.read()
                self.text_area.insert(tk.END, contents)
                self.log_count_label.config(text=f"Entries: {len(contents.splitlines())}")
        else:
            self.text_area.insert(tk.END, f"No log entries for {date}.")
            self.log_count_label.config(text="Entries: 0")

    def load_selected_log(self):
        date = self.calendar.get_date()
        self.load_log_for_date(date)

    def on_date_selected(self, event):
        self.load_selected_log()

    def toggle_logging(self):
        self.is_tracking_active = not self.is_tracking_active
        self.toggle_callback(self.is_tracking_active)
        if not self.is_tracking_active:
            from logger.disable_logger import log_disable_event
            log_disable_event()
        self.update_toggle_button()

    def update_toggle_button(self):
        if self.is_tracking_active:
            self.toggle_button.config(text="Disable Logging", bg="red", fg="white")
        else:
            self.toggle_button.config(text="Enable Logging", bg="green", fg="white")

    def auto_refresh(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        if self.selected_date == current_date:
            self.load_log_for_date(self.selected_date)
        self.root.after(5000, self.auto_refresh)
