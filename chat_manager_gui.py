import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

from core.claude_profile import Claude_Profile
from core.gemini_profile import Gemini_Profile
from core.gpt_profile import GPT_Profile
from core.ai_model_profile import AI_Model_Profile

PROFILES_FILE = "profiles.json"

def load_profiles():
    if os.path.exists(PROFILES_FILE):
        try:
            with open(PROFILES_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except Exception:
            return []
    return []

def save_profiles(profiles):
    # Guardar solo los datos serializables (no los objetos)
    data = []
    for p in profiles:
        data.append({
            "name": p.name,
            "api_key": p.api_key,
            "model": p.model,
            "ai_type": p.__class__.__name__.replace("_Profile", "").lower(),
            "history": p.history
        })
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def profile_from_dict(d):
    ai_type = d.get("ai_type", "")
    if ai_type == "claude":
        p = Claude_Profile(d["name"], d["api_key"], d["model"])
    elif ai_type == "gpt":
        p = GPT_Profile(d["name"], d["api_key"], d["model"])
    elif ai_type == "gemini":
        p = Gemini_Profile(d["name"], d["api_key"], d["model"])
    else:
        return None
    p.history = d.get("history", [])
    return p

class ProfileApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Profile Creator")

        # Widgets
        tk.Label(root, text="Nombre del perfil:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="API Key:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.api_key_entry = tk.Entry(root)
        self.api_key_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Modelo:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.model_entry = tk.Entry(root)
        self.model_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Tipo de IA:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.ai_type = ttk.Combobox(root, values=["claude", "gpt", "gemini"])
        self.ai_type.grid(row=3, column=1, padx=5, pady=5)
        self.ai_type.current(0)

        self.create_button = tk.Button(root, text="Crear Perfil", command=self.create_profile)
        self.create_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.profile_output = tk.Text(root, height=10, width=50)
        self.profile_output.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.chat_button = tk.Button(root, text="Chatear con perfil seleccionado", command=self.open_chat)
        self.chat_button.grid(row=6, column=0, columnspan=2, pady=5)

        # Cargar perfiles
        self.profiles = []
        self.load_profiles_from_file()

    def load_profiles_from_file(self):
        data = load_profiles()
        self.profiles = []
        self.profile_output.delete(1.0, tk.END)
        for d in data:
            p = profile_from_dict(d)
            if p:
                self.profiles.append(p)
                self.profile_output.insert(tk.END, f"{p.__class__.__name__} - {p.name}\n")

    def create_profile(self):
        name = self.name_entry.get()
        api_key = self.api_key_entry.get()
        model = self.model_entry.get()
        ai_type = self.ai_type.get().lower()

        if not name or not api_key or not model:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos.")
            return

        if ai_type == "claude":
            profile = Claude_Profile(name, api_key, model)
        elif ai_type == "gpt":
            profile = GPT_Profile(name, api_key, model)
        elif ai_type == "gemini":
            profile = Gemini_Profile(name, api_key, model)
        else:
            messagebox.showerror("Error", "Tipo de IA no válido.")
            return

        self.profiles.append(profile)
        self.profile_output.insert(tk.END, f"Perfil creado: {profile.__class__.__name__} - {name}\n")
        save_profiles(self.profiles)

    def open_chat(self):
        # Selección por nombre
        name = simpledialog.askstring("Seleccionar perfil", "Nombre del perfil para chatear:")
        profile = next((p for p in self.profiles if p.name == name), None)
        if not profile:
            messagebox.showerror("Error", "Perfil no encontrado.")
            return

        chat_win = tk.Toplevel(self.root)
        chat_win.title(f"Chat con {profile.name}")

        chat_text = tk.Text(chat_win, state=tk.NORMAL, height=20, width=60)
        chat_text.pack(padx=5, pady=5)
        for msg in profile.history:
            chat_text.insert(tk.END, f"{msg['role']}: {msg['content']}\n")
        chat_text.config(state=tk.DISABLED)

        entry = tk.Entry(chat_win, width=50)
        entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        def send():
            message = entry.get().strip()
            if not message:
                return
            profile.history.append({"role": "user", "content": message})
            try:
                response = profile.send_message(message)
            except Exception as e:
                response = f"Error: {e}"
            chat_text.config(state=tk.NORMAL)
            chat_text.insert(tk.END, f"user: {message}\n")
            chat_text.insert(tk.END, f"assistant: {response}\n")
            chat_text.config(state=tk.DISABLED)
            entry.delete(0, tk.END)
            save_profiles(self.profiles)

        send_btn = tk.Button(chat_win, text="Enviar", command=send)
        send_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        entry.bind("<Return>", lambda event: send())

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = ProfileApp(root)
    root.mainloop()
