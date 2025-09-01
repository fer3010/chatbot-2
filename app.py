import time
import os
import google.generativeai as genai
from flask import Flask, render_template, request

# Verifica ruta actual y contenido de templates
print("📂 Ruta actual:", os.getcwd())
print("📄 Archivos en ./templates:", os.listdir("templates"))

# Clave API gratuita
# NOTA: Por seguridad, en un entorno de producción, la clave API no debería estar codificada
API_KEY = "AIzaSyAvL_TQGMbXzKHfEi_iiwJlnwzY6jUwux4"
genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-1.5-flash-latest"

try:
    model = genai.GenerativeModel(MODEL_NAME)
    chat = model.start_chat(history=[])
    print(f"✅ Modelo cargado: {MODEL_NAME}")
except Exception as e:
    print(f"❌ Error al cargar el modelo: {e}")
    chat = None

app = Flask(__name__)

# Diccionario de respuestas locales ampliado
local_responses = {
    "hola": "¡Hola! ¿Cómo estás?",
    "quién eres": "Soy el Chat Bot de Yereexx.",
    "adiós": "¡Hasta luego!",
    "gracias": "¡De nada!",
    "cómo estás": "Estoy aquí para ayudarte, ¿en qué te puedo servir?",
    "qué puedes hacer": "Puedo responder preguntas, mantener conversaciones y ayudarte con diversas consultas.",
    "help": "Puedes preguntarme lo que quieras. Intenta saludarme o hacer una pregunta específica.",
    "modo de uso": "Escribe tu mensaje en el cuadro de texto y presiona enviar. ¡Es así de simple!",
    "nombre": "Soy YereexxBot, tu asistente virtual."
}

def obtener_respuesta_local(entrada_usuario):
    """Busca la mejor coincidencia para respuestas locales"""
    entrada = entrada_usuario.lower().strip()
    
    # Búsqueda exacta primero
    if entrada in local_responses:
        return local_responses[entrada]
    
    # Búsqueda por coincidencia parcial
    for clave, respuesta in local_responses.items():
        if clave in entrada:
            return respuesta
    
    return None

@app.route("/", methods=["GET", "POST"])
def home():
    global chat  # La corrección está aquí: la declaración global va al inicio de la función
    error = None
    historial_chat = chat.history if chat else []
    
    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        
        if not user_input:
            error = "Por favor, escribe un mensaje."
        elif not chat:
            error = "El modelo no está disponible. Intenta recargar la página."
        else:
            try:
                # Verifica si hay respuesta local
                respuesta_local = obtener_respuesta_local(user_input)
                
                if respuesta_local:
                    response_text = respuesta_local
                    chat.history.append({"role": "user", "parts": [{"text": user_input}]})
                    chat.history.append({"role": "model", "parts": [{"text": response_text}]})
                else:
                    # Pequeña pausa para evitar límites de tasa
                    time.sleep(2)
                    response = chat.send_message(user_input)
                    response_text = response.text
                
            except Exception as e:
                error = f"Ocurrió un error: {e}"
                # Intenta reiniciar la conversación si hay error
                try:
                    chat = model.start_chat(history=[])
                except:
                    pass
    
    return render_template("index.html", 
                           chat_history=historial_chat, 
                           error=error,
                           modelo_disponible=chat is not None)

@app.route("/limpiar", methods=["POST"])
def limpiar_chat():
    """Limpia el historial del chat"""
    global chat
    if model and chat:
        try:
            chat = model.start_chat(history=[])
            return "Chat limpiado correctamente"
        except Exception as e:
            return f"Error al limpiar el chat: {e}"
    return "No se pudo limpiar el chat"

if __name__ == "__main__":
    # Escucha en todas las interfaces para acceso desde red local
    app.run(host="0.0.0.0", port=5000, debug=True)