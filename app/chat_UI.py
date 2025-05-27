from PyQt5.QtWidgets import (
    QApplication, QWidget, QTextEdit, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QLabel, QDialog, QListWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class ChatUI(QWidget):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.setWindowTitle("🤖 ShopBot - Interfaz Moderna")
        self.setFixedSize(700, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Encabezado
        titulo = QLabel("💬 ShopBot")
        titulo.setFont(QFont("Segoe UI", 20, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Área de chat
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("background-color: #ecf0f1; padding: 10px; font: 12pt 'Segoe UI';")
        layout.addWidget(self.chat_area, 6)

        # Entrada y botón
        entrada_layout = QHBoxLayout()
        self.input_line = QLineEdit()
        self.input_line.setFont(QFont("Segoe UI", 11))
        self.input_line.setPlaceholderText("Escribe tu mensaje...")
        self.input_line.returnPressed.connect(self.send_message)

        enviar_btn = QPushButton("Enviar")
        enviar_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 6px 20px;")
        enviar_btn.clicked.connect(self.send_message)

        entrada_layout.addWidget(self.input_line)
        entrada_layout.addWidget(enviar_btn)
        layout.addLayout(entrada_layout)

        # Botones extra
        botones_layout = QHBoxLayout()
        config_btn = QPushButton("⚙️ Configuración")
        historial_btn = QPushButton("📜 Historial")
        frecuencia_btn = QPushButton("📊 Frecuencia")

        config_btn.clicked.connect(self.abrir_configuracion)
        historial_btn.clicked.connect(self.abrir_historial)
        frecuencia_btn.clicked.connect(self.abrir_frecuencia)

        botones_layout.addWidget(config_btn)
        botones_layout.addWidget(historial_btn)
        botones_layout.addWidget(frecuencia_btn)

        layout.addLayout(botones_layout)

        self.setLayout(layout)

    def send_message(self):
        mensaje = self.input_line.text().strip()
        if not mensaje:
            return
        respuesta = self.bot.responder("Usuario", mensaje)
        self.chat_area.append(f"<b>🧑 Usuario:</b> {mensaje}")
        self.chat_area.append(f"<b>🤖 ShopBot:</b> {respuesta}<br>")
        self.input_line.clear()

    def abrir_configuracion(self):
        ventana = ConfigWindow(self.bot, self)
        ventana.exec_()

    def abrir_historial(self):
        ventana = HistorialWindow(self.bot, self)
        ventana.exec_()

    def abrir_frecuencia(self):
        ventana = FrecuenciaWindow(self.bot, self)
        ventana.exec_()


class ConfigWindow(QDialog):
    def __init__(self, bot, parent=None):
        super().__init__(parent)
        self.bot = bot
        self.setWindowTitle("⚙️ Configurar Palabras Clave")
        self.setFixedSize(400, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.palabra_input = QLineEdit()
        self.palabra_input.setPlaceholderText("Palabra clave")
        self.respuestas_input = QLineEdit()
        self.respuestas_input.setPlaceholderText("Respuestas separadas por '|'")

        agregar_btn = QPushButton("Agregar Palabra")
        agregar_btn.clicked.connect(self.agregar_palabra)

        layout.addWidget(QLabel("Palabra clave:"))
        layout.addWidget(self.palabra_input)
        layout.addWidget(QLabel("Respuestas (separadas por '|'):"))
        layout.addWidget(self.respuestas_input)
        layout.addWidget(agregar_btn)

        self.setLayout(layout)

    def agregar_palabra(self):
        palabra = self.palabra_input.text().strip()
        respuestas = self.respuestas_input.text().strip()
        if palabra and respuestas:
            self.bot.agregar_palabra_clave(palabra, respuestas)
            QMessageBox.information(self, "Éxito", f"Palabra clave '{palabra}' agregada.")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Por favor ingresa la palabra y las respuestas.")


class HistorialWindow(QDialog):
    def __init__(self, bot, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📜 Historial de Interacciones")
        self.setFixedSize(600, 400)

        layout = QVBoxLayout()
        self.lista = QListWidget()
        historial = bot.obtener_historial()
        if historial:
            self.lista.addItems(historial)
        else:
            self.lista.addItem("No hay interacciones aún.")

        layout.addWidget(self.lista)
        self.setLayout(layout)


class FrecuenciaWindow(QDialog):
    def __init__(self, bot, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📊 Frecuencia de Uso")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        self.lista = QListWidget()
        frecuencia = bot.obtener_frecuencia_uso()
        if frecuencia:
            self.lista.addItems(frecuencia)
        else:
            self.lista.addItem("No hay palabras clave registradas.")

        layout.addWidget(self.lista)
        self.setLayout(layout)


