import os, time
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST'), database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASSWORD')
    )

def init_db():
    retries = 5
    while retries > 0:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS departamentos (id SERIAL PRIMARY KEY, nome VARCHAR(100) NOT NULL);''')
            conn.commit()
            cur.close()
            conn.close()
            break
        except Exception:
            retries -= 1
            time.sleep(2)

@app.route('/departamentos', methods=['POST'])
def criar():
    dados = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO departamentos (nome) VALUES (%s) RETURNING id;', (dados['nome'],))
    id_gerado = cur.fetchone()[0]
    conn.commit()
    return jsonify({'id': id_gerado}), 201

@app.route('/departamentos', methods=['GET'])
def listar():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM departamentos;')
    resultados = [{'id': f[0], 'nome': f[1]} for f in cur.fetchall()]
    return jsonify(resultados)

@app.route('/departamentos/<int:id>', methods=['PUT'])
def atualizar(id):
    dados = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE departamentos SET nome = %s WHERE id = %s;', (dados['nome'], id))
    conn.commit()
    return jsonify({'mensagem': 'Atualizado'})

@app.route('/departamentos/<int:id>', methods=['DELETE'])
def remover(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM departamentos WHERE id = %s;', (id,))
    conn.commit()
    return jsonify({'mensagem': 'Removido'})

@app.route('/departamentos/<int:id>', methods=['GET'])
def obter(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM departamentos WHERE id = %s;', (id,))
    dep = cur.fetchone()
    cur.close()
    conn.close()
    if dep is None:
        return jsonify({'erro': 'Não encontrado'}), 404
    return jsonify({'id': dep[0], 'nome': dep[1]})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
