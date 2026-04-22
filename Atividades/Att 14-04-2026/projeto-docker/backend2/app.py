from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    try:
        response = requests.get("https://69cf2974a4647a9fc6752317.mockapi.io/api/CLIENTES")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/health")
def health():
    return jsonify({"status": "up"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)