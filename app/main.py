from bot import Bot

from app.bot import Bot

bot = Bot("Shopbot")

while True:
    print("\n--- SHOPBOT: Menú de opciones ---")
    print("1. Agregar palabra clave y respuestas")
    print("2. Enviar mensaje al bot")
    print("3. Ver historial de interacciones")
    print("4. Ver frecuencia de uso de palabras clave")
    print("5. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        palabra = input("Ingrese la palabra clave: ")
        respuestas = input("Ingrese las respuestas separadas por '|': ")
        bot.agregar_palabra_clave(palabra, respuestas)
        print("✅ Palabra clave y respuestas añadidas.")

    elif opcion == "2":
        usuario = input("Ingrese su nombre: ")
        mensaje = input("Escriba su mensaje: ")
        respuesta = bot.responder(usuario, mensaje)
        print(f"🤖 Shopbot: {respuesta}")

    elif opcion == "3":
        bot.mostrar_historial()

    elif opcion == "4":
        bot.mostrar_frecuencia_uso()

    elif opcion == "5":
        print("👋 ¡Hasta luego!")
        break

    else:
        print("❌ Opción no válida. Intente de nuevo.")
