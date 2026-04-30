from flask import Flask, jsonify, request
app = Flask(__name__)

atividades = [
    {"id":1,"titulo":"Lista Docker","descricao":"Criar Dockerfile","aluno_id":1,"status":"pendente"}
]

@app.route("/atividades", methods=["GET"])
def listar():
    return jsonify(atividades)

@app.route("/atividades", methods=["POST"])
def criar():
    d = request.get_json()
    nova = {
        "id": len(atividades)+1,
        "titulo": d["titulo"],
        "descricao": d["descricao"],
        "aluno_id": d["aluno_id"],
        "status": d.get("status","pendente")
    }
    atividades.append(nova)
    return jsonify(nova), 201

@app.route("/atividades/aluno/<int:aid>", methods=["GET"])
def por_aluno(aid):
    return jsonify([a for a in atividades if a["aluno_id"] == aid])

@app.route("/atividades/<int:id>/concluir", methods=["PUT"])
def concluir(id):
    for a in atividades:
        if a["id"] == id:
            a["status"] = "concluida"
            return jsonify(a)
    return jsonify({"erro":"não encontrada"}),404

app.run(host="0.0.0.0", port=5001)
