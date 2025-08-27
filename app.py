from flask import Flask, request, render_template
import google.generativeai as genai
import json

# Configura tu API key
genai.configure(api_key="AIzaSyD2e0XcC7ZzEsX3oMTzTT8roY62CjqLtt4")

# Inicializa el modelo Gemini 1.5 Pro
model = genai.GenerativeModel("gemini-pro")

# Cargar respuestas locales desde responses.json
with open("responses.json", "r", encoding="utf-8") as f:
    local_responses = json.load(f)

app = Flask(__name__)

def buscar_respuesta_local(mensaje):
    mensaje = mensaje.lower()
    for categoria in local_responses:
        for clave in local_responses[categoria]:
            if clave in mensaje:
                return local_responses[categoria][clave]
    return None

@app.route("/", methods=["GET", "POST"])
def chat():
    response = None
    if request.method == "POST":
        user_input = request.form["user_input"]
        try:
            # Buscar primero en respuestas locales
            local_response = buscar_respuesta_local(user_input)
            if local_response:
                response = local_response
            else:
                # Si no hay respuesta local, usar Gemini
                chat_session = model.start_chat()
                gemini_response = chat_session.send_message(user_input)
                response = gemini_response.text
        except Exception as e:
            response = f"Error: {e}"
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)
