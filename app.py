import os
from flask import Flask, render_template, request
import google.generativeai as genai

# --- Configuración del Chatbot ---
# NOTA: Por seguridad, se recomienda guardar la clave API en una variable de entorno.
# La siguiente línea la busca en el entorno. Si prefieres colocarla aquí,
# reemplaza os.environ.get("API_KEY") por tu clave.
API_KEY = os.environ.get("API_KEY", "AIzaSyAvL_TQGMbXzKHfEi_iiwJlnwzY6jUwux4")
genai.configure(api_key=API_KEY)

MODELO_GEMINI = "gemini-1.5-flash-latest"

# Intentar cargar el modelo y la sesión de conversación al inicio
modelo = None
sesion_conversacion = None

try:
    modelo = genai.GenerativeModel(MODELO_GEMINI)
    sesion_conversacion = modelo.start_chat(history=[])
    print(f"✅ Modelo {MODELO_GEMINI} cargado y listo.")
except Exception as error_carga:
    print(f"❌ Error al cargar el modelo: {error_carga}")
    sesion_conversacion = None

# Respuestas predefinidas para optimizar el rendimiento
respuestas_rapidas = {
    "hola": "¡Hola! ¿En qué puedo ayudarte hoy?",
    "quien eres": "Soy un asistente conversacional creado por Yereexx.",
    "adios": "¡Hasta pronto! Que tengas un buen día.",
    "gracias": "Con gusto.",
    "como estas": "Estoy funcionando perfectamente, gracias por preguntar. ¿Qué necesitas?"
}

# --- Configuración de la Aplicación Flask ---
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def pagina_principal():
    mensaje_error = None
    if request.method == "POST":
        entrada_usuario = request.form.get("user_input", "").strip().lower()

        if entrada_usuario and sesion_conversacion:
            try:
                # Priorizar respuestas rápidas antes de la API
                if entrada_usuario in respuestas_rapidas:
                    respuesta_chatbot = respuestas_rapidas[entrada_usuario]
                else:
                    # Enviar mensaje a la API de Gemini
                    respuesta_chatbot = sesion_conversacion.send_message(entrada_usuario).text

                # Actualizar el historial de la conversación
                sesion_conversacion.history.append({"role": "user", "parts": [{"text": entrada_usuario}]})
                sesion_conversacion.history.append({"role": "model", "parts": [{"text": respuesta_chatbot}]})
            except Exception as fallo:
                mensaje_error = f"⚠️ Ocurrió un error: {fallo}"

    return render_template(
        "index.html",
        chat_history=sesion_conversacion.history if sesion_conversacion else [],
        error=mensaje_error
    )