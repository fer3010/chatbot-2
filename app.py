import os
import requests
from flask import Flask, request, jsonify, render_template

# Tu clave API
API_KEY = "AIzaSyD2e0XcC7ZzEsX3oMTzTT8roY62CjqLtt4"
API_URL = "https://api.openai.com/v1/chat/completions"

app = Flask(__name__)

def get_ai_response(user_message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_message}]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        
        response_data = response.json()
        ai_response = response_data['choices'][0]['message']['content'].strip()
        return ai_response
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return "Lo siento, no pude comunicarme con el servicio de IA. Inténtalo de nuevo más tarde."

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