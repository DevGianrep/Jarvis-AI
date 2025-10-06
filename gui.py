import tkinter as tk
from tkinter import ttk
import threading

class JarvisGUI:
    def __init__(self, on_user_input):
        self.root = tk.Tk()
        self.root.title("Jarvis AI HUD")
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "black")
        self.root.configure(bg='black')
        self.root.overrideredirect(True)  # Remove window border
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")

        self.on_user_input = on_user_input

        self.text_var = tk.StringVar()
        self.text_display = tk.Label(self.root, text="", font=("Consolas", 24), fg="cyan", bg="black", justify="left", wraplength=self.root.winfo_screenwidth() - 100)
        self.text_display.pack(pady=20, padx=20, anchor="nw")

        self.input_box = ttk.Entry(self.root, textvariable=self.text_var, font=("Consolas", 18))
        self.input_box.pack(fill='x', padx=20, pady=10)
        self.input_box.bind("<Return>", self._on_enter)
        self.input_box.pack_forget()  # Hide initially

        self.root.bind_all('<Control-F>', self.toggle_input_box)
        self.root.bind_all('<Control-Escape>', self.quit_app)

        self.input_visible = False

    def toggle_input_box(self, event=None):
        if self.input_visible:
            self.input_box.pack_forget()
            self.input_visible = False
        else:
            self.input_box.pack(fill='x', padx=20, pady=10)
            self.input_box.focus()
            self.input_visible = True

    def _on_enter(self, event):
        text = self.text_var.get().strip()
        if text:
            self.on_user_input(text)
            self.text_var.set("")
            if self.input_visible:
                self.toggle_input_box()

    def display_text(self, text):
        # Thread-safe update
        def update():
            self.text_display.config(text=text)
        self.root.after(0, update)

    def start(self):
        threading.Thread(target=self.root.mainloop, daemon=True).start()
