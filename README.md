# 🎓 Sistema de Gerenciamento Acadêmico — Microsserviços em Flask

Este projeto implementa um sistema acadêmico distribuído baseado em **microsserviços Flask**, projetado para gerenciar **professores, alunos, turmas, reservas de salas/laboratórios, atividades e notas**.

O sistema é dividido em três microsserviços independentes, que se comunicam entre si via requisições HTTP utilizando a biblioteca `requests`. Cada serviço possui seu próprio banco de dados SQLite, documentação Swagger e segue o padrão **MVC (Model-View-Controller)**.

## 🏗️ Arquitetura do Sistema

A arquitetura é composta por três microsserviços autônomos e interconectados:

<p align="center">
  <pre>
┌──────────────────────────────┐
│        Gerenciamento         │
│ (Professores, Turmas, Alunos)│
│ Porta: 5000                  │
│                              │
│ -> Fornece IDs para          │
│    os outros serviços        │
└───────────────┬──────────────┘
                │
                │ (HTTP Requests)
                ▼
┌───────────────┴──────────────┐
│          Reservas            │
│ (Reservas de Salas e Labs)   │
│ Porta: 5001                  │
│                              │
│ -> Usa turma_id do           │
│    serviço Gerenciamento     │
└───────────────┬──────────────┘
                │
                │ (HTTP Requests)
                ▼
┌───────────────┴──────────────┐
│          Atividades          │
│ (Atividades e Notas)         │
│ Porta: 5002                  │
│                              │
│-> Usa turma_id e professor_id│
│   do serviço Gerenciamento   │
└──────────────────────────────┘
  </pre>
</p>

### 🔹 Gerenciamento
Responsável pelo **cadastro e gerenciamento** de professores, alunos e turmas.  
Este serviço é o núcleo do sistema, pois fornece os IDs necessários para os outros microsserviços.

- **Entidades:** Professor, Aluno, Turma  
- **Função principal:** Gerar e fornecer IDs para as entidades base do sistema  
- **Banco:** `gerenciamento.db`  
- **Porta:** `5000`

### 🔹 Reservas
Gerencia as **reservas de salas e laboratórios**, associadas a turmas.  
Depende do serviço de Gerenciamento para obter o `turma_id`.

- **Entidades:** Reserva  
- **Função principal:** CRUD de reservas vinculadas a uma turma  
- **Banco:** `reservas.db`  
- **Porta:** `5001`

### 🔹 Atividades e Notas
Gerencia **atividades** e **notas** vinculadas a professores e turmas.  
Depende do serviço de Gerenciamento para obter `professor_id` e `turma_id`.

- **Entidades:** Atividade, Nota  
- **Função principal:** CRUD de atividades e notas associadas a professor e turma  
- **Banco:** `atividades.db`  
- **Porta:** `5002`

## 🔁 Integração entre Microsserviços
Os microsserviços se comunicam entre si de forma **síncrona** via **HTTP REST** utilizando a biblioteca `requests`.

### Exemplo de fluxo:
1. O microsserviço **Reservas** faz uma requisição `GET` ao **Gerenciamento** para verificar se o `turma_id` existe.  
2. O microsserviço **Atividades** faz uma requisição `GET` ao **Gerenciamento** para validar `professor_id` e `turma_id`.  
3. Caso as validações sejam bem-sucedidas, as informações são persistidas localmente em seu próprio banco SQLite.

Essa abordagem mantém **baixo acoplamento** e **independência de falhas** entre os microsserviços.

---

## ⚙️ Execução com Docker

### 📁 Estrutura de diretórios
<p align="center">
<pre>

MICROSSERVICOS_EDUCACAO/
│
├── atividades/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── Controllers.py
│   │   ├── models.py
│   │   ├── routes.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── run.py
│
├── gerenciamento/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── controllers.py
│   │   ├── models.py
│   │   ├── routes.py
│   ├── instance/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── run.py
│
├── Reserva/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── Controllers.py
│   │   ├── models.py
│   │   ├── routes.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── run.py
│
├── .gitignore
├── docker-compose.yml
├── test_crud_microservicos.py
└── README.md

</pre>
</p>


### ▶️ Passos para execução

1. **Clonar o repositório:**
   ```bash
   git clone <Link HTTPS>
   cd microsservicos_educacao

2. **Subir os microsserviços com Docker Compose**
    ```bash
    # Se estiver no Windows o DockerDesktop tem que estar aberto com a sua conta logada do github
    docker-compose up --build

3. Acessar os serviços
- **Gerenciamento:** [http://localhost:5000](http://localhost:5001)
- **Reservas:** [http://localhost:5001](http://localhost:5002)
- **Atividades:** [http://localhost:5002](http://localhost:5003)

4. Documentação Swagger (para cada serviço)
- [http://localhost:5000/swagger](http://localhost:5000/swagger)
- [http://localhost:5001/swagger](http://localhost:5001/swagger)
- [http://localhost:5002/swagger](http://localhost:5002/swagger)


## 🧠 Tecnologias Utilizadas
- **Flask** — Framework web para construção de APIs RESTful  
- **SQLAlchemy** — ORM para persistência de dados  
- **SQLite** — Banco de dados leve e local  
- **Docker / Docker Compose** — Containerização e orquestração  
- **Swagger (Flasgger)** — Documentação interativa da API  
- **Requests** — Comunicação HTTP entre serviços  

---

## 🧩 Benefícios da Arquitetura de Microsserviços
- Independência de implantação e manutenção  
- Isolamento de falhas entre serviços  
- Escalabilidade horizontal por módulo  
- Maior clareza de responsabilidades por domínio  
  (Gerenciamento, Reservas e Atividades)  

---

## 👥 Autores
Projeto desenvolvido por:  
**Eduardo Oliveira** - **RA: 2501548**,
**Analice Gomes** - **RA: 2404038** e
**Arthur Gonçalves** - **RA: 2404108**

_Faculdade Impacta Tecnologia._
