import random

class PalabraClave:
    def __init__(self, palabra, respuestas):
        self.palabra = palabra.lower()
        self.respuestas = respuestas if isinstance(respuestas, list) else [respuestas]
        self.usos = 0

    def obtener_respuesta(self):
        self.usos += 1
        return random.choice(self.respuestas)
