import os, requests
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Configuração das URLs das APIs utilizando os nomes dos serviços na rede Docker
API_DEP = "http://api-departamentos:5000/departamentos"
API_FUNC = "http://api-funcionarios:5000/funcionarios"
API_BEN = "http://api-beneficios:5000/beneficios"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Sistema RH - Docker</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f9; }
        .container { display: flex; gap: 20px; align-items: flex-start; flex-wrap: wrap; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); flex: 1; min-width: 300px; }
        h1 { text-align: center; color: #333; }
        h2 { color: #555; border-bottom: 2px solid #007bff; padding-bottom: 5px; }
        input, select { padding: 8px; margin: 5px 0; width: 100%; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; background-color: white; }
        button { padding: 8px 15px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; width: 100%; margin-top: 10px; box-sizing: border-box; }
        button:hover { background: #0056b3; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 14px; }
        th, td { padding: 8px; border-bottom: 1px solid #ddd; text-align: left; }
        th { background-color: #f8f9fa; }
        .btn-danger { background: #dc3545; padding: 4px 8px; text-decoration: none; border-radius: 3px; color: white; font-size: 12px; }
    </style>
</head>
<body>
    <h1>Sistema de Recursos Humanos</h1>
    <div class="container">
        
        <div class="card">
            <h2>Departamentos</h2>
            <form action="/add_dep" method="post">
                <input type="text" name="nome" placeholder="Nome do Departamento" required>
                <button type="submit">Cadastrar Departamento</button>
            </form>
            <table>
                <tr><th>ID</th><th>Nome</th><th>Ação</th></tr>
                {% for d in deps %}
                <tr>
                    <td>{{ d.id }}</td>
                    <td>{{ d.nome }}</td>
                    <td><a href="/del_dep/{{ d.id }}" class="btn-danger" onclick="return confirm('Confirmar exclusão de departamento?')">Excluir</a></td>
                </tr>
                {% endfor %}
            </table>
        </div>

        <div class="card">
            <h2>Funcionários</h2>
            <form action="/add_func" method="post">
                <input type="text" name="nome" placeholder="Nome do Funcionário" required>
                <input type="text" name="cargo" placeholder="Cargo" required>
                <select name="departamento_id" required>
                    <option value="" disabled selected>Selecionar Departamento...</option>
                    {% for d in deps %}
                    <option value="{{ d.id }}">{{ d.nome }} (ID: {{ d.id }})</option>
                    {% endfor %}
                </select>
                <button type="submit">Cadastrar Funcionário</button>
            </form>
            <table>
                <tr><th>ID</th><th>Nome</th><th>Cargo</th><th>ID Dep</th><th>Ação</th></tr>
                {% for f in funcs %}
                <tr>
                    <td>{{ f.id }}</td>
                    <td>{{ f.nome }}</td>
                    <td>{{ f.cargo }}</td>
                    <td>{{ f.departamento_id }}</td>
                    <td><a href="/del_func/{{ f.id }}" class="btn-danger" onclick="return confirm('Confirmar exclusão de funcionário?')">Excluir</a></td>
                </tr>
                {% endfor %}
            </table>
        </div>

        <div class="card">
            <h2>Benefícios</h2>
            <form action="/add_ben" method="post">
                <input type="text" name="nome_beneficio" placeholder="Nome do Benefício" required>
                <input type="number" step="0.01" name="valor" placeholder="Valor (R$)" required>
                <select name="funcionario_id" required>
                    <option value="" disabled selected>Selecionar Funcionário...</option>
                    {% for f in funcs %}
                    <option value="{{ f.id }}">{{ f.nome }} (ID: {{ f.id }})</option>
                    {% endfor %}
                </select>
                <button type="submit">Cadastrar Benefício</button>
            </form>
            <table>
                <tr><th>ID (Mongo)</th><th>Benefício</th><th>Valor</th><th>ID Func</th><th>Ação</th></tr>
                {% for b in bens %}
                <tr>
                    <td>{{ b._id[:8] }}...</td>
                    <td>{{ b.nome_beneficio }}</td>
                    <td>R$ {{ b.valor }}</td>
                    <td>{{ b.funcionario_id }}</td>
                    <td><a href="/del_ben/{{ b._id }}" class="btn-danger" onclick="return confirm('Confirmar exclusão de benefício?')">Excluir</a></td>
                </tr>
                {% endfor %}
            </table>
        </div>

    </div>
</body>
</html>
"""

@app.route('/')
def index():
    try: deps = requests.get(API_DEP).json()
    except: deps = []
    try: funcs = requests.get(API_FUNC).json()
    except: funcs = []
    try: bens = requests.get(API_BEN).json()
    except: bens = []
    return render_template_string(HTML_TEMPLATE, deps=deps, funcs=funcs, bens=bens)

@app.route('/add_dep', methods=['POST'])
def add_dep():
    requests.post(API_DEP, json={"nome": request.form['nome']})
    return redirect(url_for('index'))

@app.route('/del_dep/<int:id>')
def del_dep(id):
    # Verificação de dependência: impede excluir departamento se houver funcionários vinculados
    try:
        funcs_resp = requests.get(API_FUNC).json()
        if isinstance(funcs_resp, list):
            if any(str(f.get('departamento_id')) == str(id) for f in funcs_resp):
                return "<script>alert('ERRO: Não é possível excluir um departamento que possui funcionários vinculados.'); window.location.href='/';</script>"
    except Exception:
        pass
    
    requests.delete(f"{API_DEP}/{id}")
    return redirect(url_for('index'))

@app.route('/add_func', methods=['POST'])
def add_func():
    dados = {
        "nome": request.form['nome'], 
        "cargo": request.form['cargo'], 
        "departamento_id": int(request.form['departamento_id'])
    }
    requests.post(API_FUNC, json=dados)
    return redirect(url_for('index'))

@app.route('/del_func/<int:id>')
def del_func(id):
    # Verificação de dependência: impede excluir funcionário se houver benefícios vinculados
    try:
        bens_resp = requests.get(API_BEN).json()
        if isinstance(bens_resp, list):
            if any(str(b.get('funcionario_id')) == str(id) for b in bens_resp):
                return "<script>alert('ERRO: Não é possível excluir um funcionário que possui benefícios vinculados.'); window.location.href='/';</script>"
    except Exception:
        pass

    requests.delete(f"{API_FUNC}/{id}")
    return redirect(url_for('index'))

@app.route('/add_ben', methods=['POST'])
def add_ben():
    dados = {
        "nome_beneficio": request.form['nome_beneficio'], 
        "valor": float(request.form['valor']), 
        "funcionario_id": int(request.form['funcionario_id'])
    }
    requests.post(API_BEN, json=dados)
    return redirect(url_for('index'))

@app.route('/del_ben/<id>')
def del_ben(id):
    requests.delete(f"{API_BEN}/{id}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
