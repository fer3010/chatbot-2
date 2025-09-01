
import os
import time
from flask import Flask, render_template, request
import google.generativeai as genai


CLAVE_API = "AIzaSyC16OU-zOygGp74Q1kOxbxR1Uo1A68k39U"
MODELO_GEMINI = "gemini-1.5-flash-latest"
genai.configure(apikey=CLAVEAPI)


modelo = None
conversacion = None

try:
    modelo = genai.GenerativeModel(MODELO_GEMINI)
    conversacion = modelo.start_chat(history=[])
    print(f"✅ Modelo cargado correctamente: {MODELO_GEMINI}")
except Exception as error_modelo:
    print(f"⚠️ Error al iniciar el modelo: {error_modelo}")


print("📁 Carpeta actual:", os.getcwd())
print("📂 Archivos en 'templates':", os.listdir("templates"))


aplicacion = Flask(name)

@aplicacion.route("/", methods=["GET", "POST"])
def interfaz():
    mensaje_error = None
    if request.method == "POST":
        entrada = request.form.get("user_input", "").strip()
        if entrada and conversacion:
            try:
                time.sleep(5)  # ⏳ Pausa para evitar saturación
                conversacion.send_message(entrada)
            except Exception as fallo:
                mensaje_error = f"⚠️ Ocurrió un error: {fallo}"
    return rendertemplate("index.html", chathistory=conversacion.history if conversacion else [], error=mensaje_error)