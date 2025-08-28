import google.generativeai as genai
from flask import Flask, request, jsonify, render_template

# Configura tu clave API
genai.configure(api_key="AIzaSyBeLRZD1gELs7K66drGWiL0eG3Ftokw2Ss")

# Inicializa el modelo Gemini Pro
def get_model():
    try:
        available_models = [m.name for m in genai.list_models()]
        if "models/gemini-pro" in available_models:
            return genai.GenerativeModel(model_name="models/gemini-pro")
        else:
            raise ValueError("El modelo 'gemini-pro' no está disponible para esta clave API.")
    except Exception as e:
        print(f"Error al obtener el modelo: {e}")
        return None

model = get_model()

app = Flask(__name__)

# Verifica si la API está disponible
def is_api_available():
    if not model:
        return False, "Modelo no disponible o mal configurado."
    try:
        response = model.generate_content("¿Estás disponible?")
        return True, response.text.strip()
    except Exception as e:
        return False, str(e)

# Genera respuesta con control de longitud
def get_ai_response(user_message):
    if not model:
        return "Modelo no disponible."
    try:
        if len(user_message) > 1000:
            user_message = user_message[:1000]
        response = model.generate_content(user_message)
        return response.text.strip()
    except Exception as e:
        print(f"Error al generar contenido con Gemini: {e}")
        return "Hubo un problema al generar la respuesta con Gemini. Intenta más tarde."

@app.route('/')
def index():
    return render_template('index.html')  # Asegúrate de tener este archivo en /templates

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
