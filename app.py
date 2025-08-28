import google.generativeai as genai
from flask import Flask, request, jsonify, render_template

# Configura tu nueva clave API gratuita
genai.configure(api_key="AIzaSyBeLRZD1gELs7K66drGWiL0eG3Ftokw2Ss")

# Usa el modelo gemini-pro (versión 1.0, compatible con generate_content)
model = genai.GenerativeModel("gemini-pro")

app = Flask(__name__)

# Verifica si la API está disponible
def is_api_available():
    try:
        response = model.generate_content("¿Estás disponible?")
        return True, response.text.strip()
    except Exception as e:
        return False, str(e)

# Genera respuesta con control de longitud
def get_ai_response(user_message):
    try:
        # Limita el mensaje si es muy largo (ej. 1000 caracteres)
        if len(user_message) > 1000:
            user_message = user_message[:1000]

        response = model.generate_content(user_message)
        return response.text.strip()
    except Exception as e:
        print(f"Error al generar contenido con Gemini: {e}")
        return "Hubo un problema al generar la respuesta con Gemini. Intenta más tarde."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'response': 'Mensaje vacío.'})

    disponible, estado = is_api_available()
    if not disponible:
        return jsonify({'response': f"La API no está disponible: {estado}"})

    ai_response = get_ai_response(user_message)
    return jsonify({'response': ai_response})

@app.route('/test_api')
def test_api():
    disponible, estado = is_api_available()
    return jsonify({
        'status': 'ok' if disponible else 'error',
        'message': estado
    })

if __name__ == '__main__':
    app.run(debug=True)
