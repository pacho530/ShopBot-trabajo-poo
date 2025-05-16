import tkinter as tk
from tkinter import ttk, messagebox

class ChatUI(tk.Tk):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.title("ShopBot - Interfaz Profesional")
        self.geometry("700x600")
        self.resizable(False, False)

        self.crear_menu()
        self.crear_area_chat()
        self.crear_entrada_mensaje()

    def crear_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        opciones_menu = tk.Menu(menubar, tearoff=0)
        opciones_menu.add_command(label="Configuración", command=self.abrir_configuracion)
        opciones_menu.add_command(label="Historial", command=self.abrir_historial)
        opciones_menu.add_command(label="Frecuencia de Uso", command=self.abrir_frecuencia)
        opciones_menu.add_separator()
        opciones_menu.add_command(label="Salir", command=self.quit)
        menubar.add_cascade(label="Opciones", menu=opciones_menu)

    def crear_area_chat(self):
        self.chat_area = tk.Text(self, state=tk.DISABLED, bg="#1e1e1e", fg="#d4d4d4",
                                 font=("Consolas", 12), wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=(10,0), fill=tk.BOTH, expand=True)

        # Scrollbar vertical para el chat
        scrollbar = ttk.Scrollbar(self.chat_area, command=self.chat_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_area.config(yscrollcommand=scrollbar.set)

    def crear_entrada_mensaje(self):
        frame_entrada = ttk.Frame(self)
        frame_entrada.pack(fill=tk.X, padx=10, pady=10)

        self.entrada_texto = ttk.Entry(frame_entrada, font=("Consolas", 12))
        self.entrada_texto.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entrada_texto.bind("<Return>", self.enviar_mensaje)

        boton_enviar = ttk.Button(frame_entrada, text="Enviar", command=self.enviar_mensaje)
        boton_enviar.pack(side=tk.LEFT, padx=(10,0))

    def enviar_mensaje(self, event=None):
        mensaje_usuario = self.entrada_texto.get().strip()
        if not mensaje_usuario:
            return

        usuario = "Usuario"
        respuesta = self.bot.responder(usuario, mensaje_usuario)

        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"{usuario}: {mensaje_usuario}\n")
        self.chat_area.insert(tk.END, f"ShopBot: {respuesta}\n\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

        self.entrada_texto.delete(0, tk.END)

    def abrir_configuracion(self):
        ConfigWindow(self, self.bot)

    def abrir_historial(self):
        HistorialWindow(self, self.bot)

    def abrir_frecuencia(self):
        FrecuenciaWindow(self, self.bot)


class ConfigWindow(tk.Toplevel):
    def __init__(self, parent, bot):
        super().__init__(parent)
        self.bot = bot
        self.title("Configuración - Añadir Palabras Clave")
        self.geometry("400x220")
        self.resizable(False, False)

        ttk.Label(self, text="Palabra clave:", font=("Arial", 12)).pack(padx=20, pady=(20,5))
        self.entrada_palabra = ttk.Entry(self, font=("Arial", 12))
        self.entrada_palabra.pack(padx=20, pady=5, fill=tk.X)

        ttk.Label(self, text="Respuestas (separadas por '|'):", font=("Arial", 12)).pack(padx=20, pady=(15,5))
        self.entrada_respuestas = ttk.Entry(self, font=("Arial", 12))
        self.entrada_respuestas.pack(padx=20, pady=5, fill=tk.X)

        ttk.Button(self, text="Agregar Palabra Clave", command=self.agregar_palabra).pack(pady=20)

    def agregar_palabra(self):
        palabra = self.entrada_palabra.get().strip()
        respuestas = self.entrada_respuestas.get().strip()
        if not palabra or not respuestas:
            messagebox.showwarning("Error", "Debes ingresar palabra clave y respuestas.")
            return

        self.bot.agregar_palabra_clave(palabra, respuestas)
        messagebox.showinfo("Éxito", f"Palabra clave '{palabra}' agregada con éxito.")
        self.destroy()


class HistorialWindow(tk.Toplevel):
    def __init__(self, parent, bot):
        super().__init__(parent)
        self.bot = bot
        self.title("Historial de Interacciones")
        self.geometry("600x400")
        self.resizable(False, False)

        texto = tk.Text(self, bg="#f0f0f0", font=("Consolas", 11))
        texto.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        historial = self.bot.obtener_historial()
        if historial:
            for linea in historial:
                texto.insert(tk.END, linea + "\n")
        else:
            texto.insert(tk.END, "No hay interacciones aún.")

        texto.config(state=tk.DISABLED)


class FrecuenciaWindow(tk.Toplevel):
    def __init__(self, parent, bot):
        super().__init__(parent)
        self.bot = bot
        self.title("Frecuencia de Uso de Palabras Clave")
        self.geometry("400x300")
        self.resizable(False, False)

        texto = tk.Text(self, bg="#f9f9f9", font=("Consolas", 11))
        texto.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        frecuencia = self.bot.obtener_frecuencia_uso()
        if frecuencia:
            for linea in frecuencia:
                texto.insert(tk.END, linea + "\n")
        else:
            texto.insert(tk.END, "No hay palabras clave registradas.")

        texto.config(state=tk.DISABLED)





