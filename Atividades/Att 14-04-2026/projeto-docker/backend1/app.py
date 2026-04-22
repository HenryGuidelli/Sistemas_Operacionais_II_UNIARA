from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return jsonify({
    "service": "backend1",
    "description": "API de usuários",
    "status": "ok"
    })
@app.route("/health")
def health():
    return jsonify({"status": "up"})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
