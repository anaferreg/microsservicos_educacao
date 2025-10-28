# Bem vindo ao nosso projeto!

# API Flask MVC com SQLite, Swagger e Docker

Este projeto é uma API REST construída com **Flask**, usando **SQLAlchemy** como ORM e banco de dados **SQLite**. A API segue a arquitetura **MVC** (Models, Views/Controllers, Routes) e possui documentação via **Swagger**. Também é possível rodar a aplicação usando **Docker**.

---

## Arquitetura MVC

- **Models (`models.py`)**: Definem as entidades do banco de dados (ex: `Aluno`, `Professor`, `Turma`).  
- **Controllers (`controllers.py`)**: Contêm a lógica da aplicação, realizando consultas, validações e operações CRUD.  
- **Routes (`routes.py`)**: Definem os endpoints da API e chamam os métodos dos controllers.  
- **App (`__init__.py`)**: Inicializa o Flask, configura o banco de dados e registra as rotas.

O fluxo típico é:  
**Request → Route → Controller → Model → Response**

---

## Rodando localmente com venv

1. Clone o repositório:

"```bash"
git clone <URL_DO_REPOSITORIO>
cd api

Instruções para execução do projeto:

1. Realizar a inicialização do seu ambiente virtual usando:

    python -m venv venv

    .\venv\Scripts\Activate --> Windows
    
    source venv/bin/activate --> Linux

    deactivate --> Desativa o ambiente

2. Realizar a instalação das bibliotecas executando o comando:

    pip install -r requirements.txt

3. Rode a aplicação

    python run.py

4. Acesse a API em: http://localhost:5000

    A documentação Swagger estará disponível em: http://localhost:5000/apidocs

---

## Rodando com Docker 

1. Crie a imagem Docker:

	docker build -t flask_mvc_app .

2. Execute o container:

	docker run -p 5000:5000 flask_mvc_app

3. Acesse a API em: http://localhost:5000

	Swagger: http://localhost:5000/apidocs

---

## Observações

- Banco de dados SQLite local (escola.db) é criado automaticamente ao rodar a aplicação.

- Para novos modelos, adicione na models.py e migre as alterações.

- Swagger/Flasgger facilita testar a API diretamente pelo navegador.