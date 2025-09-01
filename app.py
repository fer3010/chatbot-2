import time
import os
import google.generativeai as genai
from flask import Flask, render_template, request

# Verificación de la ruta y contenido de la carpeta de templates
print("📂 Ruta actual:", os.getcwd())
print("📄 Archivos en ./templates:", os.listdir("templates"))

# Clave API
API_KEY_CHATBOT = "AIzaSyAvL_TQGMbXzKHfEi_iiwJlnwzY6jUwux4"
genai.configure(api_key=API_KEY_CHATBOT)

GEMINI_MODEL_ID = "gemini-1.5-flash-latest"

gemini_model = None
chat_session = None

try:
    gemini_model = genai.GenerativeModel(GEMINI_MODEL_ID)
    chat_session = gemini_model.start_chat(history=[])
    print(f"✅ Modelo cargado: {GEMINI_MODEL_ID}")
except Exception as e:
    print(f"❌ Error al cargar el modelo: {e}")
    chat_session = None

flask_app = Flask(__name__)

# Diccionario de respuestas predefinidas
predefined_responses = {
    "hola": "¡Hola! ¿Cómo estás?",
    "quién eres": "Soy el Chat Bot de Yereexx.",
    "adiós": "¡Hasta luego!",
    "gracias": "¡De nada!",
    "cómo estás": "Estoy aquí para ayudarte, ¿en qué te puedo servir?"
}

@flask_app.route("/", methods=["GET", "POST"])
def index():
    error_message = None
    if request.method == "POST":
        user_message = request.form.get("user_input", "").strip().lower()
        if user_message and chat_session:
            try:
                # Verifica si hay una respuesta predefinida
                if user_message in predefined_responses:
                    chatbot_response = predefined_responses[user_message]
                    chat_session.history.append({"role": "user", "parts": [{"text": user_message}]})
                    chat_session.history.append({"role": "model", "parts": [{"text": chatbot_response}]})
                else:
                    time.sleep(5)  # Evita el error 429 por cuota
                    chat_session.send_message(user_message)
            except Exception as e:
                error_message = f"Ocurrió un error: {e}"
    return render_template("index.html", chat_history=chat_session.history if chat_session else [], error=error_message)
