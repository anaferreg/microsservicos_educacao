🎓 Sistema de Gerenciamento Acadêmico — Microsserviços em Flask
📘 Descrição Geral

Este projeto implementa um sistema acadêmico distribuído baseado em microsserviços Flask, projetado para gerenciar:

Professores
Alunos
Turmas
Reservas de salas/laboratórios

Atividades e Notas
O sistema é dividido em três microsserviços independentes, que se comunicam entre si via requisições HTTP (biblioteca requests).
Cada serviço possui seu próprio banco de dados SQLite, documentação Swagger, e segue o padrão MVC (Model-View-Controller).

🧠 Arquitetura do Sistema
A arquitetura é composta por três microsserviços autônomos e interconectados:
<img width="198" height="543" alt="image" src="https://github.com/user-attachments/assets/bf87154c-ca3f-46d0-a39c-4e19f1266a63" />
