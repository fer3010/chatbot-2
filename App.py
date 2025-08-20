from flask import Flask, render_template,request,jsonify
import requests
import json
import os

app = Flask(__name__)
API_KEY= os.environ.get('API_KEY')
API_URL= ""