# 🎓 Sistema de Gerenciamento Acadêmico — Microsserviços em Flask

Este projeto implementa um sistema acadêmico distribuído baseado em **microsserviços Flask**, projetado para gerenciar **professores, alunos, turmas, reservas de salas/laboratórios, atividades e notas**.

O sistema é dividido em três microsserviços independentes, que se comunicam entre si via requisições HTTP utilizando a biblioteca `requests`. Cada serviço possui seu próprio banco de dados SQLite, documentação Swagger e segue o padrão **MVC (Model-View-Controller)**.

## 🏗️ Arquitetura do Sistema

A arquitetura é composta por três microsserviços autônomos e interconectados:

<p align="center">
  <img src="https://github.com/user-attachments/assets/bf87154c-ca3f-46d0-a39c-4e19f1266a63"
       alt="Diagrama de Arquitetura dos Microsserviços"
       width="750">
</p>

### 🔹 Gerenciamento
Responsável pelo **cadastro e gerenciamento** de professores, alunos e turmas.  
Este serviço é o núcleo do sistema, pois fornece os IDs necessários para os outros microsserviços.

- **Entidades:** Professor, Aluno, Turma  
- **Função principal:** Gerar e fornecer IDs para as entidades base do sistema  
- **Banco:** `gerenciamento.db`  
- **Porta:** `5001`

### 🔹 Reservas
Gerencia as **reservas de salas e laboratórios**, associadas a turmas.  
Depende do serviço de Gerenciamento para obter o `turma_id`.

- **Entidades:** Reserva  
- **Função principal:** CRUD de reservas vinculadas a uma turma  
- **Banco:** `reservas.db`  
- **Porta:** `5002`

### 🔹 Atividades e Notas
Gerencia **atividades** e **notas** vinculadas a professores e turmas.  
Depende do serviço de Gerenciamento para obter `professor_id` e `turma_id`.

- **Entidades:** Atividade, Nota  
- **Função principal:** CRUD de atividades e notas associadas a professor e turma  
- **Banco:** `atividades.db`  
- **Porta:** `5003`

## 🔁 Integração entre Microsserviços

Os serviços se comunicam entre si de forma **síncrona**, através de **requisições HTTP REST** com a biblioteca `requests`.

<p align="center">
  <strong>Fluxo de Integração entre Microsserviços</strong>
</p>

<p align="center">
  <pre>
     ┌───────────────────────────────┐
     │         GERENCIAMENTO         │
     │  (Professores, Turmas, Alunos)│
     │           Porta 5001          │
     └───────────────┬───────────────┘
                     │ fornece IDs via HTTP (GET/POST)
                     ▼
     ┌───────────────────────────────┐
     │            RESERVAS           │
     │ (Salas e Laboratórios)        │
     │         Porta 5002            │
     └───────────────┬───────────────┘
                     │ usa turma_id fornecido
                     ▼
     ┌───────────────────────────────┐
     │       ATIVIDADES / NOTAS      │
     │ (Vincula Professor e Turma)   │
     │          Porta 5003           │
     └───────────────────────────────┘
  </pre>
</p>

Cada microsserviço funciona de forma **independente**, mas compartilha informações através de **requisições HTTP REST**.  
Essa integração é feita de maneira **síncrona**, utilizando a biblioteca `requests` do Python para chamadas entre APIs.

Por exemplo:
- O serviço **Reservas** valida uma turma antes de criar uma nova reserva, fazendo:
