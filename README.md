Sistema de Gerenciamento Acadêmico — Microsserviços em Flask


Descrição Geral

Este projeto implementa um sistema acadêmico distribuído baseado em microsserviços Flask, projetado para gerenciar:

Professores

Alunos

Turmas

Reservas de salas/laboratórios

Atividades e Notas

O sistema é dividido em três microsserviços independentes, que se comunicam entre si via requisições HTTP (biblioteca requests).
Cada serviço possui seu próprio banco de dados SQLite, documentação Swagger, e segue o padrão MVC (Model-View-Controller).



Arquitetura do Sistema
A arquitetura é composta por três microsserviços autônomos e interconectados:

┌──────────────────────────────┐
│        Gerenciamento         │
│ (Professores, Turmas, Alunos)│
│ Porta: 5001                  │
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
│ Porta: 5002                  │
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
│ Porta: 5003                  │
│                              │
│ -> Usa turma_id e professor_id│
│    do serviço Gerenciamento   │
└──────────────────────────────┘



Padrão Utilizado: MVC

Cada microsserviço segue o padrão Model-View-Controller:

Model: Define as entidades e interage com o banco via SQLAlchemy.

Controller: Contém a lógica de negócio e integração entre APIs.

View/Routes: Define as rotas Flask e retorna as respostas HTTP.



Descrição dos Microsserviços


Gerenciamento

Responsável pelo cadastro e controle de Professores, Alunos e Turmas.

Banco: gerenciamento.db

Porta: 5001

Entidades:

Professor(id, nome, idade, materia, observacoes)

Turma(id, descricao, professor_id, ativo)

Aluno(id, nome, idade, turma_id, data_nascimento)

Rotas Principais:

Método	Rota	Descrição
GET	/professores	Lista todos os professores
POST	/professores	Cadastra um novo professor
GET	/alunos	Lista todos os alunos
POST	/turmas	Cria uma nova turma
GET	/turmas/<id>	Retorna uma turma específica (usado por outros microsserviços)


Reservas

Gerencia as reservas de salas e laboratórios associadas a uma turma.

Banco: reservas.db

Porta: 5002

Entidades:

Reserva(id, num_sala, lab, data, turma_id)

Rotas Principais:

Método	Rota	Descrição
GET	/reservas	Lista todas as reservas
POST	/reservas	Cria uma nova reserva
PUT	/reservas/<id>	Atualiza uma reserva existente
DELETE	/reservas/<id>	Remove uma reserva

Integração:

Antes de criar uma reserva, o serviço de Reservas valida o turma_id chamando o microsserviço de Gerenciamento:

response = requests.get(f"http://gerenciamento:5001/turmas/{turma_id}")
if response.status_code != 200:
    abort(400, "Turma inválida")


Atividades

Gerencia atividades e notas dos alunos.

Banco: atividades.db

Porta: 5003

Entidades:

Atividade(id, nome_atividade, descricao, peso_percento, data_entrega, turma_id, professor_id)

Nota(id, nota, aluno_id, atividade_id)

Rotas Principais:

Método	Rota	Descrição
GET	/atividades	Lista todas as atividades
POST	/atividades	Cadastra uma nova atividade
GET	/notas	Lista as notas lançadas
POST	/notas	Registra uma nova nota

Integração:

Valida turma_id e professor_id via chamadas ao serviço de Gerenciamento antes de criar atividades.

Pode consultar alunos para associar notas corretamente.



Ecossistema de Microsserviços

Cada serviço é independente, possuindo seu próprio banco e ciclo de vida.
A integração ocorre via HTTP Requests, garantindo baixo acoplamento e alta coesão.

Serviço	Depende de	Tipo de Comunicação	Objetivo
Gerenciamento	—	—	Fornece IDs e dados principais
Reservas	Gerenciamento	Síncrona (requests)	Valida turma_id
Atividades	Gerenciamento	Síncrona (requests)	Valida professor_id e turma_id

Essa estrutura permite que cada microsserviço:

Seja escalável individualmente.

Seja implantado e atualizado separadamente.

Tenha banco de dados independente (evitando interferência entre domínios).

Execução com Docker
Pré-requisitos

Docker instalado

Docker Compose instalado



Passos de Execução

Clone o projeto:

git clone https://github.com/seuusuario/sistema-academico-flask.git
cd sistema-academico-flask

Execute o Docker Compose:

docker compose up --build



Acesse cada microsserviço em seu navegador:

Serviço	Porta	Documentação Swagger
Gerenciamento	http://localhost:5001	http://localhost:5001/docs
Reservas	http://localhost:5002	http://localhost:5002/docs
Atividades	http://localhost:5003	http://localhost:5003/docs

Todos os containers estarão em rede compartilhada e podem se comunicar via hostname:

gerenciamento:5001

reservas:5002

atividades:5003



Comunicação entre Serviços

A comunicação é síncrona, utilizando a biblioteca requests.
Os serviços fazem requisições diretas uns aos outros para validar IDs ou consultar informações.

Exemplo (Atividades → Gerenciamento):

import requests

def validar_professor(professor_id):
    url = f"http://gerenciamento:5001/professores/{professor_id}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Professor não encontrado")



Tecnologias Utilizadas

Python 3.11+

Flask

Flask-SQLAlchemy

Flask-Swagger-UI

Requests

SQLite

Docker / Docker Compose



Conclusão

O projeto implementa um ecossistema completo de microsserviços Flask com:

Independência de dados e lógica

Integração via APIs RESTful

Documentação com Swagger

Execução unificada via Docker Compose

Essa abordagem garante modularidade, escalabilidade e facilidade de manutenção, sendo ideal para ambientes acadêmicos e corporativos distribuídos.