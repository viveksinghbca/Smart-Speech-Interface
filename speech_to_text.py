import tkinter as tk
from tkinter import ttk, messagebox
import threading
import pyttsx3
import speech_recognition as sr

class TextSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎙️ Text & Speech Converter")
        self.root.geometry("800x550")
        self.root.resizable(True, True)

        self.dark_mode = tk.BooleanVar(value=False)
        self.mode = tk.StringVar(value="TTS")
        self.language = tk.StringVar(value="en-IN")  # Default to English

        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()

        self.setup_ui()

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(self.main_frame, text="🧠 Smart Speech Interface", font=("Segoe UI", 20, "bold"))
        title.pack(pady=(0, 10))

        self.mode_selector = ttk.Frame(self.main_frame)
        self.mode_selector.pack(pady=5)
        ttk.Radiobutton(self.mode_selector, text="Text to Speech", variable=self.mode, value="TTS", command=self.switch_mode).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(self.mode_selector, text="Speech to Text", variable=self.mode, value="STT", command=self.switch_mode).pack(side=tk.LEFT, padx=10)

        self.language_selector = ttk.Frame(self.main_frame)
        self.language_selector.pack(pady=(5, 10))
        ttk.Label(self.language_selector, text="🌐 Language:").pack(side=tk.LEFT, padx=(0, 10))
        lang_dropdown = ttk.Combobox(self.language_selector, textvariable=self.language, state="readonly", values=["en-IN", "hi-IN"])
        lang_dropdown.pack(side=tk.LEFT)

        self.text_input = tk.Text(self.main_frame, height=10, wrap=tk.WORD, font=("Segoe UI", 12), relief=tk.FLAT, bd=4)
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=(10, 10))

        self.status_label = ttk.Label(self.main_frame, text="", font=("Segoe UI", 10, "italic"))
        self.status_label.pack()

        self.action_button = ttk.Button(self.main_frame, text="🔊 Speak", command=self.run_action)
        self.action_button.pack(pady=10)

        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(20, 0))

        self.toggle_button = ttk.Checkbutton(
            footer_frame,
            text="Dark Mode",
            variable=self.dark_mode,
            command=self.toggle_theme
        )
        self.toggle_button.pack(anchor=tk.E)

        self.toggle_theme()
        self.switch_mode()

    def run_action(self):
        self.status_label.config(text="🔄 Processing... Please wait")
        threading.Thread(target=self.process_action).start()

    def process_action(self):
        if self.mode.get() == "TTS":
            text = self.text_input.get("1.0", tk.END).strip()
            if text:
                self.engine.say(text)
                self.engine.runAndWait()
                self.status_label.config(text="✅ Done Speaking")
            else:
                self.status_label.config(text="⚠️ No text entered")
        else:
            try:
                with sr.Microphone() as source:
                    self.status_label.config(text="🎧 Listening...")
                    audio = self.recognizer.listen(source, timeout=5)
                    self.status_label.config(text="💭 Recognizing...")
                    lang_code = self.language.get()
                    text = self.recognizer.recognize_google(audio, language=lang_code)
                    self.text_input.delete("1.0", tk.END)
                    self.text_input.insert(tk.END, text)
                    self.status_label.config(text="✅ Speech to Text Complete")
            except sr.WaitTimeoutError:
                self.status_label.config(text="⚠️ Listening timed out. Try again")
            except sr.UnknownValueError:
                self.status_label.config(text="❌ Could not understand audio")
            except Exception as e:
                self.status_label.config(text=f"❗ Error: {e}")

    def switch_mode(self):
        mode = self.mode.get()
        self.action_button.config(text="🔊 Speak" if mode == "TTS" else "🎤 Listen")
        self.status_label.config(text=f"🛠️ Mode: {'Text to Speech' if mode == 'TTS' else 'Speech to Text'}")

    def toggle_theme(self):
        dark = self.dark_mode.get()
        if dark:
            bg = "#1a1a2e"
            fg = "#f7f7f7"
            widget_bg = "#2e2e3e"
        else:
            bg = "#f0faff"
            fg = "#1a1a2e"
            widget_bg = "#ffffff"

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg)
        style.configure("TCheckbutton", background=bg, foreground=fg)
        style.configure("TButton", background=widget_bg, foreground=fg)
        style.configure("TRadiobutton", background=bg, foreground=fg)
        style.configure("TCombobox", fieldbackground=widget_bg, background=widget_bg, foreground=fg)

        self.root.configure(bg=bg)
        self.text_input.configure(bg=widget_bg, fg=fg, insertbackground=fg, highlightthickness=1, highlightbackground=fg)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextSpeechApp(root)
    root.mainloop()
