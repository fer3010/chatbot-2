import time
import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Verifica ruta actual y contenido de templates
print("📂 Ruta actual:", os.getcwd())
print("📄 Archivos en ./templates:", os.listdir("templates"))

# Clave API gratuita
# NOTA: Por seguridad, en un entorno de producción, la clave API no debería estar codificada
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("❌ La clave API no está configurada. Por favor, establece la variable de entorno API_KEY.")
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

@app.route("/", methods=["GET"])
def home():
    global chat
    historial_chat = chat.history if chat else []
    return render_template("index.html", 
                           chat_history=historial_chat, 
                           error=None,
                           modelo_disponible=chat is not None)

@app.route("/chat", methods=["POST"])
def get_chat_response():
    global chat
    if not chat:
        return jsonify({"error": "El modelo no está disponible."}), 503

    data = request.json
    user_input = data.get("user_input", "").strip()
    
    if not user_input:
        return jsonify({"error": "Por favor, escribe un mensaje."}), 400

    try:
        time.sleep(1) # Pequeña pausa para evitar límites de tasa
        response = chat.send_message(user_input)
        response_text = response.text
        return jsonify({"response": response_text})

    except Exception as e:
        print(f"Ocurrió un error en el API: {e}")
        try:
            # Intenta reiniciar la conversación si hay error
            chat = model.start_chat(history=[])
        except Exception as reset_e:
            print(f"Error al reiniciar el chat: {reset_e}")
        return jsonify({"error": "Ocurrió un error. El chat se ha reiniciado."}), 500

@app.route("/limpiar", methods=["POST"])
def limpiar_chat():
    """Limpia el historial del chat"""
    global chat
    if model and chat:
        try:
            chat = model.start_chat(history=[])
            return "Chat limpiado correctamente", 200
        except Exception as e:
            return f"Error al limpiar el chat: {e}", 500
    return "No se pudo limpiar el chat", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)