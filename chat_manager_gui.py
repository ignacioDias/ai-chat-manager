import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
from tkinter import simpledialog

PROFILES_FILE = "./profiles.json"

# Cargar perfiles desde profiles.json si existe
def load_profiles():
    if os.path.exists(PROFILES_FILE):
        try:
            with open(PROFILES_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except Exception:
            return {}
    return {}

# Guardar perfiles en profiles.json
def save_profiles():
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)

profiles = load_profiles()

class ChatManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Perfiles de Chat")
        self.selected_profile = None

        # Frame de perfiles
        self.profile_frame = tk.Frame(root)
        self.profile_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.profile_listbox = tk.Listbox(self.profile_frame)
        self.profile_listbox.pack()
        self.profile_listbox.bind('<<ListboxSelect>>', self.on_profile_select)

        self.add_profile_btn = tk.Button(self.profile_frame, text="Crear Perfil", command=self.create_profile)
        self.add_profile_btn.pack(pady=5)

        # Frame de chat
        self.chat_frame = tk.Frame(root)
        self.chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.chat_text = tk.Text(self.chat_frame, state=tk.DISABLED, height=20)
        self.chat_text.pack(fill=tk.BOTH, expand=True)

        self.message_entry = tk.Entry(self.chat_frame)
        self.message_entry.pack(fill=tk.X, pady=5)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_btn = tk.Button(self.chat_frame, text="Enviar", command=self.send_message)
        self.send_btn.pack()

        # Cargar perfiles existentes en la lista
        for name in profiles:
            self.profile_listbox.insert(tk.END, name)

    def create_profile(self):
        name = simpledialog.askstring("Nombre del perfil", "Introduce el nombre del perfil:")
        if not name:
            return
        if name in profiles:
            messagebox.showerror("Error", "El perfil ya existe.")
            return
        api_key = simpledialog.askstring("API Key", "Introduce la API Key:")
        model = simpledialog.askstring("Modelo", "Introduce el modelo:", initialvalue="gpt")
        model = simpledialog.askstring("Modelo", "Selecciona el modelo (gpt, gemini, claude):", initialvalue="gpt")
        # Use a simple dialog with validation

        class ModelChoiceDialog(simpledialog.Dialog):
            def body(self, master):
                tk.Label(master, text="Selecciona el modelo:").pack()
                self.var = tk.StringVar(value="gpt")
                for option in ["gpt", "gemini", "claude"]:
                    tk.Radiobutton(master, text=option, variable=self.var, value=option).pack(anchor="w")
                return None

            def apply(self):
                self.result = self.var.get()

        dialog = ModelChoiceDialog(self.root)
        model = dialog.result if dialog.result else "gpt"
        profiles[name] = {"api_key": api_key, "model": model, "history": []}
        self.profile_listbox.insert(tk.END, name)
        save_profiles()

    def on_profile_select(self, event):
        selection = self.profile_listbox.curselection()
        if selection:
            index = selection[0]
            self.selected_profile = self.profile_listbox.get(index)
            self.update_chat()

    def update_chat(self):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.delete(1.0, tk.END)
        if self.selected_profile:
            history = profiles[self.selected_profile]["history"]
            for msg in history:
                self.chat_text.insert(tk.END, f"{msg['role']}: {msg['content']}\n")
        self.chat_text.config(state=tk.DISABLED)

    def send_message(self, event=None):
        if not self.selected_profile:
            messagebox.showwarning("Sin perfil", "Selecciona un perfil primero.")
            return
        message = self.message_entry.get().strip()
        if not message:
            return
        profiles[self.selected_profile]["history"].append({"role": "user", "content": message})
        # Aquí puedes integrar la llamada real a tu modelo, por ejemplo:
        # respuesta = tu_modelo.send_message(message)
        respuesta = f"Respuesta simulada para: {message}"
        profiles[self.selected_profile]["history"].append({"role": "assistant", "content": respuesta})
        self.message_entry.delete(0, tk.END)
        self.update_chat()
        save_profiles()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatManagerApp(root)
    root.mainloop()