import time
import os
import google.generativeai as genai
from flask import Flask, render_template, request

# Verifica ruta actual y contenido de templates
print("📂 Ruta actual:", os.getcwd())
print("📄 Archivos en ./templates:", os.listdir("templates"))

# Clave API gratuita
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

@app.route("/", methods=["GET", "POST"])
def home():
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
                # Pequeña pausa para evitar límites de tasa
                time.sleep(2)
                response = chat.send_message(user_input)
                response_text = response.text
                
            except Exception as e:
                error = f"Ocurrió un error: {e}"
                # Intenta reiniciar la conversación si hay error
                try:
                    global chat
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