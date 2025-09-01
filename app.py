import os
import google.generativeai as genai
from flask import Flask, render_template, request

# Cargar la clave API desde una variable de entorno por seguridad
API_KEY = os.environ.get("AIzaSyC16OU-zOygGp74Q1kOxbxR1Uo1A68k39U")
genai.configure(api_key=API_KEY)

MODEL_ID = "gemini-1.5-flash-latest"

try:
    chatbot_model = genai.GenerativeModel(MODEL_ID)
    chatbot_session = chatbot_model.start_chat(history=[])
    print(f"✅ Modelo cargado: {MODEL_ID}")
except Exception as e:
    print(f"❌ Error al cargar el modelo: {e}")
    chatbot_session = None

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def main_page():
    error_message = None
    if request.method == "POST":
        user_message = request.form.get("user_input", "").strip().lower()
        if user_message and chatbot_session:
            try:
                if user_message in preset_responses:
                    response_text = preset_responses[user_message]
                    chatbot_session.history.append({"role": "user", "parts": [{"text": user_message}]})
                    chatbot_session.history.append({"role": "model", "parts": [{"text": response_text}]})
                else:
                    chatbot_session.send_message(user_message)
            except Exception as e:
                error_message = f"Ocurrió un error: {e}"
    
    return render_template("index.html", chat_history=chatbot_session.history if chatbot_session else [], error=error_message)