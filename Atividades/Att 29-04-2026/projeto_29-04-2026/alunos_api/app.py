from flask import Flask, jsonify, request
app = Flask(__name__)

alunos = [
    {"id": 1, "nome": "João Silva", "curso": "Sistemas de Informação"},
    {"id": 2, "nome": "Maria Oliveira", "curso": "Engenharia de Computação"}
]

@app.route("/alunos", methods=["GET"])
def listar_alunos():
    return jsonify(alunos)

@app.route("/alunos", methods=["POST"])
def cadastrar_aluno():
    dados = request.get_json()
    novo = {"id": len(alunos)+1, "nome": dados["nome"], "curso": dados["curso"]}
    alunos.append(novo)
    return jsonify(novo), 201

@app.route("/alunos/<int:id>", methods=["GET"])
def buscar(id):
    for a in alunos:
        if a["id"] == id:
            return jsonify(a)
    return jsonify({"erro": "Aluno não encontrado"}), 404

app.run(host="0.0.0.0", port=5000)
