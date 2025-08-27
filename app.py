import time
import os
import json
import google.generativeai as genai
from flask import Flask, render_template, request

# Verifica ruta actual y contenido de templates
print("📂 Ruta actual:", os.getcwd())
print("📄 Archivos en ./templates:", os.listdir("templates"))

# Clave API gratuita
API_KEY = "AIzaSyD2e0XcC7ZzEsX3oMTzTT8roY62CjqLtt4"
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

# Cargar respuestas locales desde JSON
try:
    with open("local_responses.json", "r", encoding="utf-8") as f:
        local_responses = json.load(f)
    print("✅ Respuestas locales cargadas desde JSON")
except Exception as e:
    print(f"❌ Error al cargar el archivo JSON: {e}")
    local_responses = {}

@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip().lower()
        if user_input and chat:
            try:
                # Verifica si hay respuesta local
                if user_input in local_responses:
                    response_text = local_responses[user_input]
                    chat.history.append({"role": "user", "parts": [{"text": user_input}]})
                    chat.history.append({"role": "model", "parts": [{"text": response_text}]})
                else:
                    time.sleep(5)  # evita error 429 por cuota
                    chat.send_message(user_input)
            except Exception as e:
                error = f"Ocurrió un error: {e}"
    return render_template("index.html", chat_history=chat.history if chat else [], error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)