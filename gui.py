import tkinter as tk
from tkinter import ttk
import threading
from voice_control import listen_for_command
from gesture_control import GestureControl
from commands import execute_command

class PCControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart PC Control")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#0D1B2A")

        self.is_listening = False

        self.custom_font = ("Segoe UI", 14)

        self.main_frame = tk.Frame(root, bg="#1B263B")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", width=1000, height=700)

        # TITLE
        tk.Label(
            self.main_frame,
            text="🎛 Smart PC Controller",
            font=("Segoe UI", 28, "bold"),
            fg="white",
            bg="#1B263B"
        ).pack(pady=20)

        # STATUS LABEL
        self.status_label = tk.Label(
            self.main_frame,
            text="Status: Idle",
            font=self.custom_font,
            fg="#00FFAA",
            bg="#1B263B"
        )
        self.status_label.pack(pady=10)

        # COMMAND DISPLAY BOX
        self.command_box = tk.Text(
            self.main_frame,
            height=5,
            width=60,
            font=("Segoe UI", 12),
            bg="#0D1B2A",
            fg="white"
        )
        self.command_box.pack(pady=15)

        # VOICE BUTTON
        self.voice_button = ttk.Button(
            self.main_frame,
            text="🎤 Start Voice Control",
            command=self.toggle_voice,
        )
        self.voice_button.pack(pady=10)

        # GESTURE BUTTON
        self.gesture_button = ttk.Button(
            self.main_frame,
            text="✋ Start Gesture Control",
            command=self.start_gesture_thread
        )
        self.gesture_button.pack(pady=10)

        # EXIT BUTTON
        ttk.Button(
            self.main_frame,
            text="❌ Exit",
            command=self.stop_all
        ).pack(pady=20)

        # STYLE
        style = ttk.Style()
        style.configure(
            "TButton",
            font=("Segoe UI", 13),
            padding=10
        )

        self.gesture_control = GestureControl()

    # ---------------- VOICE CONTROL ----------------

    def toggle_voice(self):
        if not self.is_listening:
            self.is_listening = True
            self.status_label.config(text="Status: Listening 🎤")
            threading.Thread(target=self.voice_loop).start()
        else:
            self.is_listening = False
            self.status_label.config(text="Status: Stopped")

    def voice_loop(self):
        while self.is_listening:
            command = listen_for_command()

            if command:
                self.update_command_box(command)
                execute_command(command)

    def update_command_box(self, command):
        self.command_box.insert(tk.END, f"> {command}\n")
        self.command_box.see(tk.END)

    # ---------------- GESTURE CONTROL ----------------

    def start_gesture_thread(self):
        threading.Thread(target=self.gesture_control.start).start()

    # ---------------- EXIT ----------------

    def stop_all(self):
        self.is_listening = False
        self.gesture_control.stop()
        self.root.quit()