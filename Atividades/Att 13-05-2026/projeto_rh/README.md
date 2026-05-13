# Sistema de RH - Aplicação Distribuída com Containers

[cite_start]**Disciplina:** Sistemas Operacionais [cite: 3]  
**Grupo:** * Henry Guidelli - 04724-556
* Murilo Paiva Garbelini - 04724-557

## Sobre o Projeto
[cite_start]Este projeto é uma solução computacional para um Sistema de Recursos Humanos (RH) desenvolvido como atividade prática[cite: 1, 6, 17, 31]. [cite_start]O ambiente simula uma arquitetura de microsserviços real [cite: 6][cite_start], utilizando containers Docker orquestrados para demonstrar a comunicação de redes internas, persistência de dados em volumes e o consumo entre APIs RESTful independentes[cite: 8, 10, 11].

O ecossistema é composto por **6 containers** rodando simultaneamente:
1. [cite_start]**postgres-db**: Banco de dados relacional (PostgreSQL) para dados estruturados de departamentos e funcionários[cite: 42].
2. [cite_start]**mongo-db**: Banco de dados NoSQL (MongoDB) para dados flexíveis de benefícios[cite: 43].
3. [cite_start]**api-departamentos**: API em Python (Flask) responsável pela gestão dos departamentos, armazenando no PostgreSQL[cite: 39, 50, 52].
4. [cite_start]**api-funcionarios**: API em Python (Flask) responsável pela gestão de funcionários[cite: 39, 50, 52]. [cite_start]Comunica-se via rede Docker com a `api-departamentos` para validar a existência do departamento antes do cadastro no PostgreSQL[cite: 60].
5. [cite_start]**api-beneficios**: API em Python (Flask) responsável pela gestão de benefícios[cite: 39, 50, 52]. [cite_start]Comunica-se via rede Docker com a `api-funcionarios` para validar a existência do funcionário antes da concessão do benefício no MongoDB[cite: 60].
6. **frontend-web**: Aplicação Web Server-Side (Flask/HTML) encapsulada em um container que atua como interface visual do sistema, orquestrando as interações do usuário diretamente com as APIs pelo backend.

## Funcionalidades e Diferenciais
* [cite_start]**CRUD Completo:** Operações de Cadastro, Consulta, Atualização (via rotas estruturadas) e Remoção distribuídas e isoladas entre as respectivas APIs[cite: 54, 55, 56, 57, 58].
* **Interface Integrada:** Tela única e responsiva no navegador com formulários dinâmicos (Comboboxes) que carregam as chaves estrangeiras em tempo real das APIs de origem.
* **Integridade Referencial (Travas de Segurança):** O sistema previne a exclusão de registros que possuem dependências (ex: impede apagar um departamento se houver funcionários vinculados a ele, ou apagar um funcionário com benefícios ativos).
* [cite_start]**Isolamento de Rede:** Comunicação entre os microsserviços feita exclusivamente pela rede interna do Docker (bridge)[cite: 10].

## Como Executar
1. Certifique-se de ter o Docker e o Docker Compose instalados no seu sistema operacional.
2. [cite_start]Pelo terminal, navegue até o diretório raiz do projeto (onde está o arquivo `docker-compose.yml`)[cite: 70].
3. Execute o comando para construir as imagens e subir todo o ambiente em segundo plano:
   ```bash
   docker-compose up -d --build
