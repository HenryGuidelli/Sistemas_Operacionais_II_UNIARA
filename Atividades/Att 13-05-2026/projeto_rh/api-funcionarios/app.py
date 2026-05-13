import os, time, requests
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)
API_DEPARTAMENTOS_URL = os.environ.get('API_DEPARTAMENTOS_URL', 'http://api-departamentos:5000')

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'rh_database'),
        user=os.environ.get('DB_USER', 'admin'),
        password=os.environ.get('DB_PASSWORD', 'adminpassword')
    )

def init_db():
    retries = 5
    while retries > 0:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS funcionarios (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    cargo VARCHAR(100) NOT NULL,
                    departamento_id INTEGER NOT NULL
                );
            ''')
            conn.commit()
            cur.close()
            conn.close()
            break
        except Exception:
            retries -= 1
            time.sleep(2)

@app.route('/funcionarios', methods=['POST'])
def criar_funcionario():
    novo_func = request.get_json()
    dep_id = novo_func.get('departamento_id')
    
    # Valida se o departamento existe na API de Departamentos
    try:
        resposta = requests.get(f"{API_DEPARTAMENTOS_URL}/departamentos/{dep_id}")
        if resposta.status_code != 200:
            return jsonify({'erro': 'Departamento não encontrado na API de Departamentos'}), 404
    except Exception as e:
        return jsonify({'erro': 'Erro de conexão com API Departamentos'}), 500

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO funcionarios (nome, cargo, departamento_id) VALUES (%s, %s, %s) RETURNING id;',
                (novo_func['nome'], novo_func['cargo'], dep_id))
    func_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': func_id, 'mensagem': 'Funcionário criado com sucesso'}), 201

@app.route('/funcionarios', methods=['GET'])
def listar_funcionarios():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM funcionarios;')
    funcionarios = [{'id': f[0], 'nome': f[1], 'cargo': f[2], 'departamento_id': f[3]} for f in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(funcionarios)

@app.route('/funcionarios/<int:id>', methods=['GET'])
def obter_funcionario(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM funcionarios WHERE id = %s;', (id,))
    func = cur.fetchone()
    cur.close()
    conn.close()
    if func is None:
        return jsonify({'erro': 'Não encontrado'}), 404
    return jsonify({'id': func[0], 'nome': func[1], 'cargo': func[2], 'departamento_id': func[3]})

@app.route('/funcionarios/<int:id>', methods=['PUT'])
def atualizar_funcionario(id):
    dados = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE funcionarios SET nome = %s, cargo = %s, departamento_id = %s WHERE id = %s;',
                (dados['nome'], dados['cargo'], dados['departamento_id'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensagem': 'Atualizado com sucesso'})

@app.route('/funcionarios/<int:id>', methods=['DELETE'])
def remover_funcionario(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM funcionarios WHERE id = %s;', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensagem': 'Removido com sucesso'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
