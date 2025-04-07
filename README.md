
# 🤖 Shopbot - Bot de Automatización para Redes Sociales

Shopbot es una aplicación que automatiza respuestas e interacciones en redes sociales para tiendas online. Esta herramienta mejora la atención al cliente, sugiere productos y genera respuestas rápidas mediante palabras clave.

---

## 🧩 Descomposición de Requisitos Funcionales

A continuación, se presenta la descomposición de los requisitos funcionales definidos para la aplicación **Shopbot**, junto con su asignación de responsabilidades a clases y métodos:

### 📋 Tabla de descomposición

| Requisito Funcional | Subfuncionalidades | Clase Responsable | Método(s) encargado(s) |
|---------------------|--------------------|--------------------|-------------------------|
| **RF1. Registrar palabras clave** | - Solicitar palabra clave<br>- Solicitar respuesta(s)<br>- Guardar la palabra y sus respuestas | `Bot` | `agregar_palabra_clave()` |
| **RF2. Responder automáticamente** | - Analizar el mensaje del usuario<br>- Verificar si contiene palabra clave<br>- Seleccionar una respuesta<br>- Registrar la interacción | `Bot`, `PalabraClave`, `Interaccion` | `responder()`, `obtener_respuesta()` |
| **RF3. Mostrar historial de interacciones** | - Recorrer la lista de interacciones<br>- Mostrar usuario, mensaje y respuesta | `Bot`, `Interaccion` | `mostrar_historial()` |
| **RF4. Mostrar frecuencia de uso de palabras clave** | - Recorrer palabras clave<br>- Mostrar cuántas veces se ha usado cada una | `Bot`, `PalabraClave` | `mostrar_frecuencia_uso()` |
| **RF5. Seleccionar una respuesta aleatoria** | - Escoger al azar una respuesta entre las posibles<br>- Aumentar el contador de usos | `PalabraClave` | `obtener_respuesta()` |
| **RF6. Interfaz por consola** | - Mostrar menú<br>- Ejecutar acciones según la opción del usuario | `main.py` | Menú interactivo |
| **RF7. Permitir múltiples respuestas por palabra clave** | - Recibir varias respuestas separadas por `|`<br>- Almacenarlas como lista<br>- Elegir aleatoriamente una | `PalabraClave`, `Bot` | `agregar_palabra_clave()`, `obtener_respuesta()` |

---

### ✨ Observación

Cada requisito funcional ha sido analizado y descompuesto en tareas específicas, siguiendo los principios de la programación orientada a objetos. Esta estructura favorece la escalabilidad, reutilización de código y claridad del sistema.
