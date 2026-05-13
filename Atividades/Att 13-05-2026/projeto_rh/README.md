# Sistema de RH - Aplicação Distribuída com Containers

**Disciplina:** Sistemas Operacionais  
**Grupo:** Henry Guidelli - 04724-556 - Murilo Paiva Garbelini - 04724-557

## Sobre o Projeto
Este projeto é uma solução computacional para um Sistema de Recursos Humanos (RH) desenvolvido como atividade prática. O ambiente simula uma arquitetura de microsserviços real, utilizando containers Docker orquestrados para demonstrar a comunicação de redes internas, persistência de dados em volumes e o consumo entre APIs RESTful independentes.

O ecossistema é composto por **6 containers** rodando simultaneamente:
1. **postgres-db**: Banco de dados relacional (PostgreSQL) para dados estruturados de departamentos e funcionários.
2. **mongo-db**: Banco de dados NoSQL (MongoDB) para dados flexíveis de benefícios.
3. **api-departamentos**: API em Python (Flask) responsável pela gestão dos departamentos, armazenando no PostgreSQL.
4. **api-funcionarios**: API em Python (Flask) responsável pela gestão de funcionários. Comunica-se via rede Docker com a `api-departamentos` para validar a existência do departamento antes do cadastro no PostgreSQL.
5. **api-beneficios**: API em Python (Flask) responsável pela gestão de benefícios. Comunica-se via rede Docker com a `api-funcionarios` para validar a existência do funcionário antes da concessão do benefício no MongoDB.
6. **frontend-web**: Aplicação Web Server-Side (Flask/HTML) encapsulada em um container que atua como interface visual do sistema, orquestrando as interações do usuário diretamente com as APIs pelo backend.

## Funcionalidades e Diferenciais
* **CRUD Completo:** Operações de Cadastro, Consulta, Atualização (via rotas estruturadas) e Remoção distribuídas e isoladas entre as respectivas APIs.
* **Interface Integrada:** Tela única e responsiva no navegador com formulários dinâmicos (Comboboxes) que carregam as chaves estrangeiras em tempo real das APIs de origem.
* **Integridade Referencial (Travas de Segurança):** O sistema previne a exclusão de registros que possuem dependências (ex: impede apagar um departamento se houver funcionários vinculados a ele, ou apagar um funcionário com benefícios ativos).
* **Isolamento de Rede:** Comunicação entre os microsserviços feita exclusivamente pela rede interna do Docker (bridge).

## Como Executar
1. Certifique-se de ter o Docker e o Docker Compose instalados no seu sistema operacional.
2. Pelo terminal, navegue até o diretório raiz do projeto (onde está o arquivo `docker-compose.yml`).
3. Execute o comando para construir as imagens e subir todo o ambiente em segundo plano:
   ```bash
   docker-compose up -d --build
