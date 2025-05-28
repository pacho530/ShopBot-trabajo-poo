# bot.py

class Bot:
    def __init__(self, nombre):
        self.nombre = nombre
        self.reglas = []

    def set_reglas(self, reglas):
        """
        Actualiza la lista de reglas del bot.
        Cada regla es un diccionario con:
            - palabra: la palabra clave a buscar
            - tipo: 'Palabra exacta' o 'Contiene la palabra'
            - respuesta: el texto de respuesta que debe dar el bot
        """
        self.reglas = reglas

    def responder(self, usuario, mensaje):
        """
        Recibe el nombre del usuario y el mensaje recibido.
        Retorna la respuesta según las reglas o un mensaje por defecto.
        """
        mensaje_lower = mensaje.lower()

        for regla in self.reglas:
            palabra = regla["palabra"].lower()
            tipo = regla["tipo"]
            respuesta = regla["respuesta"]

            if tipo == "Palabra exacta":
                if mensaje_lower == palabra:
                    return respuesta

            elif tipo == "Contiene la palabra":
                if palabra in mensaje_lower:
                    return respuesta

        return "No entendí, ¿puedes reformular?"







