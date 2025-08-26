from flask import Flask, render_template, request, jsonify
import requests
import os

app= Flask (__name__)
API_KEY = os.environ.get('API_KEY')
API_URL=
.env 
API_KEY=
@app.route('/')
def home():
    return render_template("index.html")
@app.route("/get",methods=['POST'])
def get_bot_response_route():
    user_data=request.get_json()
    user_text=user_data.get('msg')
    if not user_text:
        return jsonify({"error": "No hay mensaje"}), 400
    payload = {
        "inputs": user_text
    }
