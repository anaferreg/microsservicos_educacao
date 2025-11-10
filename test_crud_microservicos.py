import requests
import sys

BASES = {
    'gerenciamento': 'http://localhost:5000',
    'reserva': 'http://localhost:5001',
    'atividades': 'http://localhost:5002',
}

def print_status(msg, ok):
    print(f"{'[OK]' if ok else '[FAIL]'} {msg}")
    if not ok:
        sys.exit(1)

def test_gerenciamento():
    print("\n--- Testando gerenciamento ---")
    # CREATE professor
    prof = {'nome': 'Prof Teste', 'idade': 40, 'materia': 'Matematica'}
    r = requests.post(f"{BASES['gerenciamento']}/professores", json=prof)
    print_status('Criar professor', r.status_code == 201)
    prof_id = r.json()['id']

    # CREATE turma
    turma = {'descricao': 'Turma Teste', 'professor_id': prof_id}
    r = requests.post(f"{BASES['gerenciamento']}/turmas", json=turma)
    print_status('Criar turma', r.status_code == 201)
    turma_id = r.json()['id']

    # CREATE aluno
    aluno = {'nome': 'Aluno Teste', 'idade': 15, 'turma_id': turma_id, 'data_nascimento': '2010-05-10'}
    r = requests.post(f"{BASES['gerenciamento']}/alunos", json=aluno)
    print_status('Criar aluno', r.status_code == 201)
    aluno_id = r.json()['id']

    # UPDATE aluno
    r = requests.put(f"{BASES['gerenciamento']}/alunos/{aluno_id}", json={'nome': 'Aluno Atualizado'})
    print_status('Atualizar aluno', r.status_code == 200 and r.json()['nome'] == 'Aluno Atualizado')

    # GET aluno
    r = requests.get(f"{BASES['gerenciamento']}/alunos/{aluno_id}")
    print_status('Buscar aluno', r.status_code == 200)

    # DELETE aluno
    r = requests.delete(f"{BASES['gerenciamento']}/alunos/{aluno_id}")
    print_status('Deletar aluno', r.status_code == 204)

    # DELETE turma
    r = requests.delete(f"{BASES['gerenciamento']}/turmas/{turma_id}")
    print_status('Deletar turma', r.status_code == 204)

    # DELETE professor
    r = requests.delete(f"{BASES['gerenciamento']}/professores/{prof_id}")
    print_status('Deletar professor', r.status_code == 204)

def test_reserva():
    print("\n--- Testando reserva ---")
    # Precisa de uma turma válida
    prof = {'nome': 'Prof Reserva', 'idade': 41, 'materia': 'Física'}
    r = requests.post(f"{BASES['gerenciamento']}/professores", json=prof)
    prof_id = r.json()['id']
    turma = {'descricao': 'Turma Reserva', 'professor_id': prof_id}
    r = requests.post(f"{BASES['gerenciamento']}/turmas", json=turma)
    turma_id = r.json()['id']
    reserva = {'num_sala': 201, 'lab': True, 'data': '2025-11-20', 'turma_id': turma_id}
    r = requests.post(f"{BASES['reserva']}/reservas", json=reserva)
    print_status('Criar reserva', r.status_code == 201)
    reserva_id = r.json()['id']
    # UPDATE
    r = requests.put(f"{BASES['reserva']}/reservas/{reserva_id}", json={'num_sala': 202})
    print_status('Atualizar reserva', r.status_code == 200 and r.json()['num_sala'] == 202)
    # GET
    r = requests.get(f"{BASES['reserva']}/reservas/{reserva_id}")
    print_status('Buscar reserva', r.status_code == 200)
    # DELETE
    r = requests.delete(f"{BASES['reserva']}/reservas/{reserva_id}")
    print_status('Deletar reserva', r.status_code == 204)
    # Limpeza
    requests.delete(f"{BASES['gerenciamento']}/turmas/{turma_id}")
    requests.delete(f"{BASES['gerenciamento']}/professores/{prof_id}")

def test_atividades():
    print("\n--- Testando atividades ---")
    # Precisa de turma e professor válidos
    prof = {'nome': 'Prof Ativ', 'idade': 42, 'materia': 'Química'}
    r = requests.post(f"{BASES['gerenciamento']}/professores", json=prof)
    prof_id = r.json()['id']
    turma = {'descricao': 'Turma Ativ', 'professor_id': prof_id}
    r = requests.post(f"{BASES['gerenciamento']}/turmas", json=turma)
    turma_id = r.json()['id']
    atividade = {'nome_atividade': 'Prova', 'descricao': 'Desc', 'peso_porcento': 30, 'data_entrega': '2025-12-01', 'turma_id': turma_id, 'professor_id': prof_id}
    r = requests.post(f"{BASES['atividades']}/atividades", json=atividade)
    print_status('Criar atividade', r.status_code == 201)
    atividade_id = r.json()['id']
    # UPDATE
    r = requests.put(f"{BASES['atividades']}/atividades/{atividade_id}", json={'descricao': 'Nova Desc'})
    print_status('Atualizar atividade', r.status_code == 200 and r.json()['descricao'] == 'Nova Desc')
    # GET
    r = requests.get(f"{BASES['atividades']}/atividades/{atividade_id}")
    print_status('Buscar atividade', r.status_code == 200)
    # DELETE
    r = requests.delete(f"{BASES['atividades']}/atividades/{atividade_id}")
    print_status('Deletar atividade', r.status_code == 204)
    # Limpeza
    requests.delete(f"{BASES['gerenciamento']}/turmas/{turma_id}")
    requests.delete(f"{BASES['gerenciamento']}/professores/{prof_id}")

def main():
    test_gerenciamento()
    test_reserva()
    test_atividades()
    print("\nTodos os testes CRUD passaram com sucesso!")

if __name__ == "__main__":
    main()
""