from app.palabra_clave import PalabraClave
from app.interaccion import Interaccion

class Bot:
    def __init__(self, nombre):
        self.nombre = nombre
        self.palabras_clave = []
        self.interacciones = []

    def agregar_palabra_clave(self, palabra, respuestas):
        respuestas_lista = [r.strip() for r in respuestas.split("|")]
        nueva = PalabraClave(palabra, respuestas_lista)
        self.palabras_clave.append(nueva)

    def responder(self, usuario, mensaje_usuario):
        mensaje = mensaje_usuario.lower()
        respuestas = []

        for palabra_clave in self.palabras_clave:
            if palabra_clave.palabra in mensaje:
                respuesta = palabra_clave.obtener_respuesta()
                respuestas.append(respuesta)

        if respuestas:
            respuesta_final = " ".join(respuestas)
        else:
            respuesta_final = "Lo siento, no entendí tu mensaje."

        self.interacciones.append(Interaccion(usuario, mensaje_usuario, respuesta_final))
        return respuesta_final

    def obtener_historial(self):
        historial = []
        for interaccion in self.interacciones:
            historial.append(f"{interaccion.usuario}: {interaccion.mensaje} => {interaccion.respuesta}")
        return historial

    def obtener_frecuencia_uso(self):
        frecuencia = []
        for pc in sorted(self.palabras_clave, key=lambda x: x.usos, reverse=True):
            frecuencia.append(f"'{pc.palabra}': {pc.usos} usos")
        return frecuencia



