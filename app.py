import os
from flask import Flask, render_template, request
import google.generativeai as genai

# Cargar la clave API directamente en el código
CLAVE_API = "AIzaSyC16OU-zOygGp74Q1kOxbxR1Uo1A68k39U"
genai.configure(api_key=CLAVE_API)

MODELO_GEMINI = "gemini-1.5-flash-latest"

modelo = None
conversacion = None

try:
    modelo = genai.GenerativeModel(MODELO_GEMINI)
    conversacion = modelo.start_chat(history=[])
    print(f"✅ Modelo cargado correctamente: {MODELO_GEMINI}")
except Exception as error_modelo:
    print(f"⚠️ Error al iniciar el modelo: {error_modelo}")

# Respuestas predefinidas para optimizar la velocidad
preset_responses = {
    "hola": "¡Hola! ¿En qué puedo ayudarte hoy?",
    "quien eres": "Soy un asistente conversacional creado por Yereexx.",
    "adios": "¡Hasta pronto! Que tengas un buen día.",
    "gracias": "Con gusto.",
    "como estas": "Estoy funcionando perfectamente, gracias por preguntar. ¿Qué necesitas?"
}

aplicacion = Flask(__name__)

@aplicacion.route("/", methods=["GET", "POST"])
def interfaz():
    mensaje_error = None
    if request.method == "POST":
        entrada = request.form.get("user_input", "").strip().lower()
        if entrada and conversacion:
            try:
                # Comprobar si existe una respuesta predefinida
                if entrada in preset_responses:
                    response_text = preset_responses[entrada]
                    conversacion.history.append({"role": "user", "parts": [{"text": entrada}]})
                    conversacion.history.append({"role": "model", "parts": [{"text": response_text}]})
                else:
                    conversacion.send_message(entrada)
            except Exception as fallo:
                mensaje_error = f"⚠️ Ocurrió un error: {fallo}"
    
    # La variable se llama 'chat_history' para que el HTML la reconozca
    return render_template("index.html", chat_history=conversacion.history if conversacion else [], error=mensaje_error)
