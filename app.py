import time
import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
import logging
from datetime import datetime
import html

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verifica ruta actual y contenido de templates
print("📂 Ruta actual:", os.getcwd())
if os.path.exists("templates"):
    print("📄 Archivos en ./templates:", os.listdir("templates"))
else:
    print("❌ No existe la carpeta templates")

# Clave API - en producción debería estar en variables de entorno
API_KEY = "AIzaSyAvL_TQGMbXzKHfEi_iiwJlnwzY6jUwux4"
genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-1.5-flash-latest"

# Intentar cargar el modelo con reintentos
def initialize_model(retries=3, delay=2):
    for attempt in range(retries):
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            chat = model.start_chat(history=[])
            print(f"✅ Modelo cargado: {MODEL_NAME}")
            return model, chat
        except Exception as e:
            print(f"❌ Intento {attempt + 1} falló: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print("❌ Todos los intentos fallaron. Usando modo sin conexión.")
                return None, None

model, chat = initialize_model()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-key-para-desarrollo')

# Diccionario de respuestas locales ampliado
local_responses = {
    "hola": "¡Hola! ¿En qué puedo ayudarte hoy?",
    "quién eres": "Soy el Chat Bot de Yereexx, basado en Gemini AI de Google.",
    "adiós": "¡Hasta luego! Fue un placer ayudarte.",
    "gracias": "¡De nada! Estoy aquí cuando me necesites.",
    "cómo estás": "¡Funcionando perfectamente! Listo para ayudarte.",
    "qué puedes hacer": "Puedo responder preguntas, mantener conversaciones y ayudarte con diversas consultas.",
    "help": "Puedes preguntarme lo que quieras. Intenta saludarme o hacer una pregunta específica.",
    "modo de uso": "Escribe tu mensaje en el cuadro de texto y presiona enviar. ¡Es así de simple!",
    "nombre": "Soy YereexxBot, tu asistente virtual.",
    "hora": f"Son las {datetime.now().strftime('%H:%M')}.",
    "día": f"Hoy es {datetime.now().strftime('%d/%m/%Y')}."
}

def get_local_response(user_input):
    """Busca la mejor coincidencia para respuestas locales"""
    user_input = user_input.lower().strip()
    
    # Búsqueda exacta
    if user_input in local_responses:
        return local_responses[user_input]
    
    # Búsqueda parcial
    for key, response in local_responses.items():
        if key in user_input:
            return response
    
    return None

@app.route("/", methods=["GET"])
def home():
    """Página principal"""
    return render_template("index.html", 
                          chat_history=chat.history if chat else [], 
                          model_loaded=chat is not None)

@app.route("/chat", methods=["POST"])
def chat_message():
    """Endpoint para manejar mensajes del chat"""
    if not chat:
        return jsonify({"error": "Modelo no disponible. Intenta recargar la página."})
    
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"error": "Mensaje vacío"})
    
    # Prevenir inyección de HTML/JS
    user_input = html.escape(user_input)
    
    try:
        # Verificar si hay respuesta local primero
        local_response = get_local_response(user_input)
        if local_response:
            # Agregar al historial
            chat.history.append({"role": "user", "parts": [{"text": user_input}]})
            chat.history.append({"role": "model", "parts": [{"text": local_response}]})
            
            return jsonify({
                "response": local_response,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })
        
        # Si no hay respuesta local, usar el modelo de Gemini
        time.sleep(1)  # Pequeña pausa para evitar límites de tasa
        
        response = chat.send_message(user_input)
        response_text = response.text
        
        return jsonify({
            "response": response_text,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        
    except Exception as e:
        logger.error(f"Error en chat: {str(e)}")
        return jsonify({
            "error": f"Lo siento, ocurrió un error: {str(e)}. Intenta de nuevo."
        })

@app.route("/clear", methods=["POST"])
def clear_chat():
    """Endpoint para limpiar el historial del chat"""
    global chat
    try:
        if model:
            chat = model.start_chat(history=[])
            return jsonify({"success": True})
        else:
            return jsonify({"error": "Modelo no disponible"})
    except Exception as e:
        return jsonify({"error": f"Error al limpiar chat: {str(e)}"})

@app.route("/status", methods=["GET"])
def status():
    """Endpoint para verificar el estado del servicio"""
    return jsonify({
        "model_loaded": chat is not None,
        "model_name": MODEL_NAME if chat else "None",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    # Obtener puerto de variable de entorno o usar 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    
    # Escucha en todas las interfaces para acceso desde red local
    app.run(host="0.0.0.0", port=port, debug=False)  # Debug False para producción