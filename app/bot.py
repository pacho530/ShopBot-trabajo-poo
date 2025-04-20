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

    def mostrar_historial(self):
        print("\n🧾 Historial de interacciones:")
        for i, interaccion in enumerate(self.interacciones, 1):
            print(f"{i}. {interaccion.usuario}: {interaccion.mensaje} => {interaccion.respuesta}")

    def mostrar_frecuencia_uso(self):
        print("\n📊 Frecuencia de uso de palabras clave:")
        if not self.palabras_clave:
            print("No hay palabras clave registradas.")
            return
        for pc in sorted(self.palabras_clave, key=lambda x: x.usos, reverse=True):
            print(f"- '{pc.palabra}': {pc.usos} usos")


