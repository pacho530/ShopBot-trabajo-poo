import customtkinter as ctk
from app.bot import Bot
import json
import os  # Necesario para verificar si el archivo existe


class BotVentasApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración ventana
        self.title("🤖 Bot de Ventas Automatizado")
        self.geometry("1200x800")
        self.resizable(True, True)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Instancia del bot
        self.bot = Bot("ShopBot")

        # Datos internos
        self.reglas = []  # Lista de diccionarios: {"palabra":..., "tipo":..., "respuesta":...}
        self.productos = []  # Lista de diccionarios: {"nombre":..., "precio":..., "tallas":..., "cantidad":...}
        self.regla_editando = None  # Para saber si estamos editando
        self.producto_editando = None  # Para saber si estamos editando un producto

        # Archivo para guardar/cargar los datos
        self.data_file = "bot_data.json"  # Nombre del archivo donde se guardarán las configuraciones

        # Crear widgets
        self.create_widgets()

        # Cargar datos al inicio de la aplicación
        self.load_data()

        # Configurar el protocolo de cierre de la ventana para guardar datos
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        sidebar = ctk.CTkFrame(self, width=80, corner_radius=0, fg_color="#2c3e50")
        sidebar.grid(row=0, column=0, sticky="nsew")

        logo_label = ctk.CTkLabel(sidebar, text="🤖", font=ctk.CTkFont(size=24))
        logo_label.pack(pady=(20, 30))

        self.btn_chat = ctk.CTkButton(sidebar, text="💬", width=40, height=40,
                                      command=self.show_chat, fg_color="transparent",
                                      hover_color="#34495e", corner_radius=5)
        self.btn_chat.pack(pady=5)

        self.btn_config = ctk.CTkButton(sidebar, text="⚙️", width=40, height=40,
                                        command=self.show_config, fg_color="transparent",
                                        hover_color="#34495e", corner_radius=5)
        self.btn_config.pack(pady=5)

        self.btn_inventario = ctk.CTkButton(sidebar, text="📦", width=40, height=40,
                                            command=self.show_inventario, fg_color="transparent",
                                            hover_color="#34495e", corner_radius=5)
        self.btn_inventario.pack(pady=5)

        salir_btn = ctk.CTkButton(sidebar, text="🚪", width=40, height=40,
                                  command=self.quit, fg_color="transparent",
                                  hover_color="#e74c3c", corner_radius=5)
        salir_btn.pack(side="bottom", pady=20)

        # Panel Principal
        self.main_panel = ctk.CTkFrame(self, corner_radius=0)
        self.main_panel.grid(row=0, column=1, sticky="nsew")
        self.main_panel.grid_rowconfigure(0, weight=1)
        self.main_panel.grid_columnconfigure(0, weight=1)

        # Vistas
        self.create_chat_view()
        self.create_config_view()
        self.create_inventario_view()

        self.show_chat()

    # --- Persistencia de Datos ---
    def load_data(self):
        """Carga las reglas y productos desde el archivo JSON."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.reglas = data.get("reglas", [])
                    self.productos = data.get("productos", [])
            except json.JSONDecodeError:
                print(f"Advertencia: El archivo {self.data_file} está corrupto o vacío. Iniciando con datos vacíos.")
                self.reglas = []
                self.productos = []

        # Asegúrate de que el bot tenga las reglas cargadas al inicio
        self.bot.set_reglas(self.reglas)
        self.actualizar_tabla_keywords()
        self.actualizar_tabla_inventario()

    def save_data(self):
        """Guarda las reglas y productos actuales en el archivo JSON."""
        data = {
            "reglas": self.reglas,
            "productos": self.productos
        }
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4,
                      ensure_ascii=False)  # `indent=4` para formato legible, `ensure_ascii=False` para caracteres especiales

    def on_closing(self):
        """Método llamado cuando la ventana se cierra para guardar los datos."""
        self.save_data()
        self.destroy()

    # -- CHAT --
    def create_chat_view(self):
        self.chat_frame = ctk.CTkFrame(self.main_panel, fg_color="transparent")

        self.chat_display = ctk.CTkTextbox(self.chat_frame, wrap="word", font=("Arial", 14))
        self.chat_display.pack(fill="both", expand=True, padx=20, pady=20)

        input_frame = ctk.CTkFrame(self.chat_frame, height=60)
        input_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.user_input = ctk.CTkEntry(input_frame, placeholder_text="Escribe un mensaje...", font=("Arial", 14))
        self.user_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.user_input.bind("<Return>", self.send_message)

        send_btn = ctk.CTkButton(input_frame, text="Enviar", width=100, font=("Arial", 14), command=self.send_message)
        send_btn.pack(side="right")

    def show_chat(self):
        self.hide_all_views()
        self.chat_frame.pack(fill="both", expand=True)
        self.btn_chat.configure(fg_color="#34495e")
        self.btn_config.configure(fg_color="transparent")
        self.btn_inventario.configure(fg_color="transparent")

    def send_message(self, event=None):
        message = self.user_input.get().strip()
        if not message:
            return
        self.chat_display.insert("end", f"Tú: {message}\n")
        self.user_input.delete(0, "end")

        # Respuesta del bot
        respuesta = self.bot.responder("usuario", message)
        self.chat_display.insert("end", f"Bot: {respuesta}\n")
        self.chat_display.see("end")

    # -- CONFIGURACIÓN DE PALABRAS CLAVE --
    def create_config_view(self):
        self.config_frame = ctk.CTkFrame(self.main_panel, fg_color="transparent")

        ctk.CTkLabel(self.config_frame, text="Configuración de Respuestas Automáticas",
                     font=("Arial", 18, "bold")).pack(pady=20)

        container = ctk.CTkScrollableFrame(self.config_frame)
        container.pack(fill="both", expand=True, padx=20)
        container.grid_columnconfigure(0, weight=1)

        add_frame = ctk.CTkFrame(container, fg_color="transparent")
        add_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(add_frame, text="Agregar/Editar Regla de Respuesta:", font=("Arial", 14)).grid(row=0, column=0,
                                                                                                    columnspan=3,
                                                                                                    sticky="w", pady=5)

        ctk.CTkLabel(add_frame, text="Palabra/Frase clave:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.palabra_clave_entry = ctk.CTkEntry(add_frame)
        self.palabra_clave_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(add_frame, text="Tipo de coincidencia:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.tipo_coincidencia = ctk.CTkOptionMenu(add_frame, values=["Palabra exacta", "Contiene la palabra"])
        self.tipo_coincidencia.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.tipo_coincidencia.set("Palabra exacta")

        ctk.CTkLabel(add_frame, text="Respuesta:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.respuesta_entry = ctk.CTkEntry(add_frame)
        self.respuesta_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        btn_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        self.agregar_editar_btn = ctk.CTkButton(btn_frame, text="Agregar Regla", command=self.agregar_o_editar_regla)
        self.agregar_editar_btn.pack(side="left", padx=5)

        cancelar_btn = ctk.CTkButton(btn_frame, text="Cancelar Edición", fg_color="gray", hover_color="#555555",
                                     command=self.cancelar_edicion)
        cancelar_btn.pack(side="left", padx=5)

        ctk.CTkLabel(container, text="Reglas Configuradas:", font=("Arial", 14)).pack(anchor="w", pady=(10, 5))

        self.keywords_table = ctk.CTkFrame(container)
        self.keywords_table.pack(fill="x")

        # Cabeceras
        ctk.CTkLabel(self.keywords_table, text="Palabra Clave", font=("Arial", 12, "bold")).grid(row=0, column=0,
                                                                                                 padx=5, pady=5)
        ctk.CTkLabel(self.keywords_table, text="Tipo", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(self.keywords_table, text="Respuesta", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5,
                                                                                             pady=5)
        ctk.CTkLabel(self.keywords_table, text="Acciones", font=("Arial", 12, "bold")).grid(row=0, column=3, padx=5,
                                                                                            pady=5)

        self.actualizar_tabla_keywords()

    def agregar_o_editar_regla(self):
        palabra = self.palabra_clave_entry.get().strip()
        tipo = self.tipo_coincidencia.get()
        respuesta = self.respuesta_entry.get().strip()

        if not palabra or not respuesta:
            ctk.CTkMessagebox(title="Error", message="Palabra clave y respuesta son obligatorios.", icon="warning")
            return

        if self.regla_editando is None:
            # Agregar nueva regla
            self.reglas.append({"palabra": palabra, "tipo": tipo, "respuesta": respuesta})
        else:
            # Editar regla existente
            self.reglas[self.regla_editando] = {"palabra": palabra, "tipo": tipo, "respuesta": respuesta}
            self.regla_editando = None
            self.agregar_editar_btn.configure(text="Agregar Regla")

        self.limpiar_formulario_regla()
        self.actualizar_tabla_keywords()

        # Actualizar reglas del bot y guardar datos
        self.bot.set_reglas(self.reglas)
        self.save_data()  # Guardar los datos después de modificar las reglas

    def actualizar_tabla_keywords(self):
        # Limpiar filas anteriores
        for widget in self.keywords_table.winfo_children():
            if int(widget.grid_info().get("row", 0)) > 0:  # Ignorar la fila de cabeceras
                widget.destroy()

        for i, regla in enumerate(self.reglas):
            ctk.CTkLabel(self.keywords_table, text=regla["palabra"]).grid(row=i + 1, column=0, padx=5, pady=5)
            ctk.CTkLabel(self.keywords_table, text=regla["tipo"]).grid(row=i + 1, column=1, padx=5, pady=5)
            ctk.CTkLabel(self.keywords_table, text=regla["respuesta"]).grid(row=i + 1, column=2, padx=5, pady=5)

            edit_btn = ctk.CTkButton(self.keywords_table, text="Editar", width=60,
                                     command=lambda idx=i: self.editar_regla(idx))
            edit_btn.grid(row=i + 1, column=3, padx=(5, 2), pady=5, sticky="w")  # Ajustar padx

            del_btn = ctk.CTkButton(self.keywords_table, text="Eliminar", width=60,
                                    fg_color="#e74c3c", hover_color="#c0392b",
                                    command=lambda idx=i: self.confirmar_eliminar_regla(
                                        idx))  # Usar función de confirmación
            del_btn.grid(row=i + 1, column=3, padx=(2, 5), pady=5, sticky="e")  # Ajustar padx

    def confirmar_eliminar_regla(self, index):
        if ctk.CTkMessagebox.ask_yes_no("Confirmar Eliminación", "¿Estás seguro de que quieres eliminar esta regla?"):
            self.eliminar_regla(index)

    def editar_regla(self, index):
        regla = self.reglas[index]
        self.palabra_clave_entry.delete(0, "end")
        self.palabra_clave_entry.insert(0, regla["palabra"])

        self.tipo_coincidencia.set(regla["tipo"])

        self.respuesta_entry.delete(0, "end")
        self.respuesta_entry.insert(0, regla["respuesta"])

        self.regla_editando = index
        self.agregar_editar_btn.configure(text="Guardar Cambios")

        self.show_config()  # Asegurarse de que la vista de configuración esté activa

    def eliminar_regla(self, index):
        del self.reglas[index]
        self.actualizar_tabla_keywords()
        self.bot.set_reglas(self.reglas)
        self.save_data()  # Guardar los datos después de eliminar una regla

    def limpiar_formulario_regla(self):
        self.palabra_clave_entry.delete(0, "end")
        self.respuesta_entry.delete(0, "end")
        self.tipo_coincidencia.set("Palabra exacta")
        self.regla_editando = None
        self.agregar_editar_btn.configure(text="Agregar Regla")

    def cancelar_edicion(self):
        self.limpiar_formulario_regla()

    def show_config(self):
        self.hide_all_views()
        self.config_frame.pack(fill="both", expand=True)
        self.btn_chat.configure(fg_color="transparent")
        self.btn_config.configure(fg_color="#34495e")
        self.btn_inventario.configure(fg_color="transparent")

    # -- INVENTARIO --
    def create_inventario_view(self):
        self.inventario_frame = ctk.CTkFrame(self.main_panel, fg_color="transparent")

        ctk.CTkLabel(self.inventario_frame, text="Gestión de Inventario", font=("Arial", 18, "bold")).pack(pady=20)

        form_frame = ctk.CTkFrame(self.inventario_frame)
        form_frame.pack(fill="x", padx=20)

        # Nombre producto
        ctk.CTkLabel(form_frame, text="Nombre del producto:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.nombre_producto_entry = ctk.CTkEntry(form_frame)
        self.nombre_producto_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Precio producto
        ctk.CTkLabel(form_frame, text="Precio:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.precio_producto_entry = ctk.CTkEntry(form_frame)
        self.precio_producto_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Tallas producto
        ctk.CTkLabel(form_frame, text="Tallas disponibles (separadas por coma):").grid(row=2, column=0, sticky="e",
                                                                                       padx=5, pady=5)
        self.tallas_producto_entry = ctk.CTkEntry(form_frame)
        self.tallas_producto_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        # Cantidad producto
        ctk.CTkLabel(form_frame, text="Cantidad:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.cantidad_producto_entry = ctk.CTkEntry(form_frame)
        self.cantidad_producto_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        form_frame.grid_columnconfigure(1, weight=1)

        # Botones
        btn_frame = ctk.CTkFrame(self.inventario_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)

        self.guardar_producto_btn = ctk.CTkButton(btn_frame, text="Guardar Producto",
                                                  command=self.agregar_o_editar_producto)
        self.guardar_producto_btn.pack(side="left", padx=5)

        self.limpiar_producto_btn = ctk.CTkButton(btn_frame, text="Limpiar Formulario", fg_color="gray",
                                                  hover_color="#555555",
                                                  command=self.limpiar_formulario_producto)
        self.limpiar_producto_btn.pack(side="left", padx=5)

        # Tabla inventario
        ctk.CTkLabel(self.inventario_frame, text="Inventario Actual:", font=("Arial", 14)).pack(anchor="w", padx=20,
                                                                                                pady=(10, 5))

        self.inventario_table = ctk.CTkFrame(self.inventario_frame)
        self.inventario_table.pack(fill="both", expand=True, padx=20, pady=10)

        # Cabeceras tabla
        ctk.CTkLabel(self.inventario_table, text="Nombre", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5,
                                                                                            pady=5)
        ctk.CTkLabel(self.inventario_table, text="Precio", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5,
                                                                                            pady=5)
        ctk.CTkLabel(self.inventario_table, text="Tallas", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5,
                                                                                            pady=5)
        ctk.CTkLabel(self.inventario_table, text="Cantidad", font=("Arial", 12, "bold")).grid(row=0, column=3, padx=5,
                                                                                              pady=5)
        ctk.CTkLabel(self.inventario_table, text="Acciones", font=("Arial", 12, "bold")).grid(row=0, column=4, padx=5,
                                                                                              pady=5)

        self.actualizar_tabla_inventario()

    def agregar_o_editar_producto(self):
        nombre = self.nombre_producto_entry.get().strip()
        precio_str = self.precio_producto_entry.get().strip()
        tallas = self.tallas_producto_entry.get().strip()
        cantidad_str = self.cantidad_producto_entry.get().strip()

        if not nombre or not precio_str or not cantidad_str:
            ctk.CTkMessagebox(title="Error", message="Nombre, precio y cantidad son obligatorios.", icon="warning")
            return

        try:
            precio = float(precio_str)
            if precio < 0:
                ctk.CTkMessagebox(title="Error", message="El precio no puede ser negativo.", icon="warning")
                return
        except ValueError:
            ctk.CTkMessagebox(title="Error", message="El precio debe ser un número válido.", icon="warning")
            return

        try:
            cantidad = int(cantidad_str)
            if cantidad < 0:
                ctk.CTkMessagebox(title="Error", message="La cantidad no puede ser negativa.", icon="warning")
                return
        except ValueError:
            ctk.CTkMessagebox(title="Error", message="La cantidad debe ser un número entero.", icon="warning")
            return

        tallas_list = [t.strip().upper() for t in tallas.split(",")] if tallas else []

        producto = {
            "nombre": nombre,
            "precio": precio,
            "tallas": tallas_list,
            "cantidad": cantidad
        }

        if self.producto_editando is None:
            # Agregar nuevo producto
            self.productos.append(producto)
            ctk.CTkMessagebox(title="Éxito", message="Producto agregado correctamente.", icon="info")
        else:
            # Editar producto existente
            self.productos[self.producto_editando] = producto
            self.producto_editando = None
            self.guardar_producto_btn.configure(text="Guardar Producto")
            self.limpiar_producto_btn.configure(text="Limpiar Formulario")
            ctk.CTkMessagebox(title="Éxito", message="Producto actualizado correctamente.", icon="info")

        self.actualizar_tabla_inventario()
        self.limpiar_formulario_producto()
        self.save_data()  # Guardar los datos después de modificar los productos

    def actualizar_tabla_inventario(self):
        # Limpiar filas anteriores
        for widget in self.inventario_table.winfo_children():
            if int(widget.grid_info().get("row", 0)) > 0:  # Ignorar la fila de cabeceras
                widget.destroy()

        for i, producto in enumerate(self.productos):
            ctk.CTkLabel(self.inventario_table, text=producto["nombre"]).grid(row=i + 1, column=0, padx=5, pady=5)
            ctk.CTkLabel(self.inventario_table, text=f"${producto['precio']:.2f}").grid(row=i + 1, column=1, padx=5,
                                                                                        pady=5)
            ctk.CTkLabel(self.inventario_table, text=", ".join(producto["tallas"])).grid(row=i + 1, column=2, padx=5,
                                                                                         pady=5)
            ctk.CTkLabel(self.inventario_table, text=str(producto["cantidad"])).grid(row=i + 1, column=3, padx=5,
                                                                                     pady=5)

            edit_btn = ctk.CTkButton(self.inventario_table, text="Editar", width=60,
                                     command=lambda idx=i: self.editar_producto(idx))
            edit_btn.grid(row=i + 1, column=4, padx=(5, 2), pady=5, sticky="w")

            del_btn = ctk.CTkButton(self.inventario_table, text="Eliminar", width=60,
                                    fg_color="#e74c3c", hover_color="#c0392b",
                                    command=lambda idx=i: self.confirmar_eliminar_producto(
                                        idx))  # Usar función de confirmación
            del_btn.grid(row=i + 1, column=4, padx=(2, 5), pady=5, sticky="e")

    def confirmar_eliminar_producto(self, index):
        if ctk.CTkMessagebox.ask_yes_no("Confirmar Eliminación",
                                        "¿Estás seguro de que quieres eliminar este producto?"):
            self.eliminar_producto(index)

    def editar_producto(self, index):
        producto = self.productos[index]
        self.nombre_producto_entry.delete(0, "end")
        self.nombre_producto_entry.insert(0, producto["nombre"])

        self.precio_producto_entry.delete(0, "end")
        self.precio_producto_entry.insert(0, str(producto["precio"]))

        self.tallas_producto_entry.delete(0, "end")
        self.tallas_producto_entry.insert(0, ", ".join(producto["tallas"]))

        self.cantidad_producto_entry.delete(0, "end")
        self.cantidad_producto_entry.insert(0, str(producto["cantidad"]))

        self.producto_editando = index
        self.guardar_producto_btn.configure(text="Actualizar Producto")
        self.limpiar_producto_btn.configure(text="Cancelar Edición")

        self.show_inventario()  # Asegurarse de que la vista de inventario esté activa

    def eliminar_producto(self, index):
        del self.productos[index]
        self.actualizar_tabla_inventario()
        self.save_data()  # Guardar los datos después de eliminar un producto

    def limpiar_formulario_producto(self):
        self.nombre_producto_entry.delete(0, "end")
        self.precio_producto_entry.delete(0, "end")
        self.tallas_producto_entry.delete(0, "end")
        self.cantidad_producto_entry.delete(0, "end")
        self.producto_editando = None
        self.guardar_producto_btn.configure(text="Guardar Producto")
        self.limpiar_producto_btn.configure(text="Limpiar Formulario")

    def show_inventario(self):
        self.hide_all_views()
        self.inventario_frame.pack(fill="both", expand=True)
        self.btn_chat.configure(fg_color="transparent")
        self.btn_config.configure(fg_color="transparent")
        self.btn_inventario.configure(fg_color="#34495e")

    def hide_all_views(self):
        self.chat_frame.pack_forget()
        self.config_frame.pack_forget()
        self.inventario_frame.pack_forget()


if __name__ == "__main__":
    app = BotVentasApp()
    app.mainloop()










