import google.generativeai as genai
from flask import Flask, request, jsonify, render_template

# Configura tu clave API de Gemini
genai.configure(api_key="AIzaSyD2e0XcC7ZzEsX3oMTzTT8roY62CjqLtt4")

# Inicializa el modelo Gemini Pro
model = genai.GenerativeModel("gemini-pro")

app = Flask(__name__)

def get_ai_response(user_message):
    try:
        response = model.generate_content(user_message)
        return response.text.strip()
    except Exception as e:
        print(f"Error al generar contenido con Gemini: {e}")
        return "Hubo un problema al generar la respuesta con Gemini."

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

if __name__ == '__main__':
    app.run(debug=True)