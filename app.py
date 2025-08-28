import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
import time

# Configura tu clave API
genai.configure(api_key="AIzaSyD2e0XcC7ZzEsX3oMTzTT8roY62CjqLtt4")

# Usa el modelo gemini-pro (más estable en el plan gratuito)
model = genai.GenerativeModel("gemini-pro")

app = Flask(__name__)

# Función principal para generar respuesta
def get_ai_response(user_message):
    try:
        response = model.generate_content(user_message)
        return response.text.strip()
    except genai.types.RateLimitError as e:
        print("⚠️ Límite de cuota alcanzado. Esperando 60 segundos...")
        time.sleep(60)
        return "Has alcanzado el límite de uso. Intenta de nuevo en un momento."
    except Exception as e:
        print(f"Error al generar contenido con Gemini: {e}")
        return "Hubo un problema al generar la respuesta con Gemini."

# ✅ Función para verificar si la API está funcionando
def test_gemini_api():
    try:
        response = model.generate_content("Hola, ¿estás funcionando?")
        return True, response.text.strip()
    except Exception as e:
        return False, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'response': 'Mensaje vacío.'})
    
    ai_response = get_ai_response(user_message)
    return jsonify({'response': ai_response})

# Ruta para probar la API
@app.route('/test_api')
def test_api():
    ok, result = test_gemini_api()
    return jsonify({
        'status': 'ok' if ok else 'error',
        'message': result
    })

if __name__ == '__main__':
    app.run(debug=True)
