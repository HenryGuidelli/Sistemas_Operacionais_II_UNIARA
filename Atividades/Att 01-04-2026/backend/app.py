from flask import Flask, render_template
import requests

app = Flask(__name__)

# ====================================================================
# COLE AQUI OS LINKS DOS MOCKS QUE VOCÊ GERAR (ex: Mocky, Beeceptor)
# ====================================================================
URL_MOCK_CLIENTES = 'https://69cf2974a4647a9fc6752317.mockapi.io/api/CLIENTES'
URL_MOCK_FUNCIONARIOS = 'https://69cf2974a4647a9fc6752317.mockapi.io/api/funcionarios'

@app.route('/')
def index():
    # 1. Python consome a API de Clientes
    try:
        # timeout=5 evita que a página trave se o mock demorar a responder
        res_clientes = requests.get(URL_MOCK_CLIENTES, timeout=5)
        clientes = res_clientes.json() if res_clientes.status_code == 200 else []
    except Exception:
        clientes = [] # Retorna lista vazia se der erro ou se o link for inválido

    # 2. Python consome a API de Funcionários
    try:
        res_funcionarios = requests.get(URL_MOCK_FUNCIONARIOS, timeout=5)
        funcionarios = res_funcionarios.json() if res_funcionarios.status_code == 200 else []
    except Exception:
        funcionarios = []

    # 3. Python envia os dados obtidos diretamente para a página web
    return render_template('index.html', clientes=clientes, funcionarios=funcionarios)

if __name__ == '__main__':
    # Roda o servidor na porta 5000
    app.run(host='0.0.0.0', port=5000)
