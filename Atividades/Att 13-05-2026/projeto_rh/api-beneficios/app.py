import os, requests
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Conexão com MongoDB [cite: 65]
client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017/'))
db = client.rh_beneficios
beneficios_collection = db.beneficios

API_FUNCIONARIOS_URL = os.environ.get('API_FUNCIONARIOS_URL', 'http://localhost:5001')

@app.route('/beneficios', methods=['POST'])
def criar():
    dados = request.get_json()
    id_funcionario = dados.get('funcionario_id')
    
    # Comunicação entre containers: Valida se o funcionário existe [cite: 100]
    resposta = requests.get(f"{API_FUNCIONARIOS_URL}/funcionarios/{id_funcionario}")
    if resposta.status_code != 200:
        return jsonify({'erro': 'Funcionário não encontrado na API de Funcionários'}), 404

    resultado = beneficios_collection.insert_one(dados)
    return jsonify({'id': str(resultado.inserted_id)}), 201

@app.route('/beneficios', methods=['GET'])
def listar():
    beneficios = []
    for b in beneficios_collection.find():
        b['_id'] = str(b['_id'])
        beneficios.append(b)
    return jsonify(beneficios)

@app.route('/beneficios/<id>', methods=['PUT'])
def atualizar(id):
    dados = request.get_json()
    beneficios_collection.update_one({'_id': ObjectId(id)}, {'$set': dados})
    return jsonify({'mensagem': 'Atualizado'})

@app.route('/beneficios/<id>', methods=['DELETE'])
def remover(id):
    beneficios_collection.delete_one({'_id': ObjectId(id)})
    return jsonify({'mensagem': 'Removido'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
