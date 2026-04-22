import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    modo = os.environ.get("MODO_EXECUCAO", "Desenvolvimento")
    
    return jsonify({
    "service": "backend3",
    "description": "API de pedidos - Serviço operacional",
    "modo_atual": modo,
    "status": "ok"
    })

@app.route("/health")
def health():
    return jsonify({"status": "up"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)