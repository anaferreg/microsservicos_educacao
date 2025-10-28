from flask import Blueprint, jsonify
from .controllers import AlunoController, ProfessorController, TurmaController

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    Endpoint inicial que verifica se a API está funcionando.
    ---
    tags:
      - Status
    summary: "Verifica o status da API"
    responses:
      200:
        description: A API está online e funcionando.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "API funcionando!"
    """
    return jsonify({"message":"API funcionando!"})

# ========================================================================================
# Rotas dos Alunos
# ========================================================================================

@bp.route('/alunos', methods=['GET'])
def get_all_aluno():
    """
    Lista todos os alunos cadastrados.
    ---
    tags:
      - Alunos
    summary: "Lista todos os alunos"
    responses:
      200:
        description: Uma lista de todos os alunos.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              idade:
                type: integer
    """
    return AlunoController.get_all_aluno()

@bp.route('/alunos/<int:id>', methods=['GET'])
def get_aluno_id(id):
    """
    Busca um aluno específico pelo seu ID.
    ---
    tags:
      - Alunos
    summary: "Busca um aluno por ID"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: O ID único do aluno a ser buscado.
    responses:
      200:
        description: Aluno encontrado com sucesso.
      404:
        description: Aluno não encontrado.
    """
    return AlunoController.get_aluno_by_id(id)

@bp.route('/alunos', methods=['POST'])
def create_aluno():
    """
    Cria um novo registro de aluno.
    ---
    tags:
      - Alunos
    summary: "Cria um novo aluno"
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
              description: Nome completo do aluno.
              example: "Maria Souza"
            idade:
              type: integer
              description: Idade do aluno.
              example: 16
            turma_id:
              type: integer
              example: 1
            data_nascimento:
              type: string
              format: date
              example: "2009-01-15"
            nota_primeiro_semestre:
              type: number
              example: 7.5
            nota_segundo_semestre:
              type: number
              example: 8.0
    responses:
      201:
        description: Aluno criado com sucesso.
      400:
        description: "Dados inválidos (ex: nome faltando)."
    """
    return AlunoController.create_Aluno() 

@bp.route('/alunos/<int:id>', methods=['PUT'])
def update_a_aluno(id):
    """
    Atualiza as informações de um aluno existente.
    ---
    tags:
      - Alunos
    summary: "Atualiza um aluno por ID"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: O ID do aluno a ser atualizado.
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            idade:
              type: integer
            turma_id:
              type: integer
    responses:
      200:
        description: Aluno atualizado com sucesso.
      404:
        description: Aluno não encontrado.
    """
    return AlunoController.update_Aluno(id) 

@bp.route('/alunos/<int:id>', methods=['DELETE'])
def delete_a_aluno(id):
    """
    Deleta o registro de um aluno.
    ---
    tags:
      - Alunos
    summary: "Deleta um aluno por ID"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: O ID do aluno a ser deletado.
    responses:
      204:
        description: "Aluno deletado com sucesso (sem conteúdo de retorno)."
      404:
        description: Aluno não encontrado.
    """
    return AlunoController.delete_Aluno(id) 

# ========================================================================================
# Rotas dos Professores
# ========================================================================================

@bp.route('/professores', methods=['GET'])
def get_all_professor():
    """
    Lista todos os professores cadastrados.
    ---
    tags:
      - Professores
    summary: "Lista todos os professores"
    responses:
      200:
        description: Uma lista de todos os professores.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              materia:
                type: string
    """
    return ProfessorController.get_all_professor()

@bp.route('/professores/<int:id>', methods=['GET'])
def get_professor_id(id):
    """
    Busca um professor específico pelo seu ID.
    ---
    tags:
      - Professores
    summary: "Busca um professor por ID"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: O ID único do professor a ser buscado.
    responses:
      200:
        description: Professor encontrado com sucesso.
      404:
        description: Professor não encontrado.
    """
    return ProfessorController.get_professor_by_id(id)

@bp.route('/professores', methods=['POST'])
def create_a_new_professor():
    """
    Cria um novo registro de professor.
    ---
    tags:
      - Professores
    summary: "Cria um novo professor"
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nome
            - materia
          properties:
            nome:
              type: string
              example: "Alberto Santos"
            idade:
              type: integer
              example: 42
            materia:
              type: string
              example: "Física"
            observacoes:
              type: string
              example: "Doutorado em física quântica."
    responses:
      201:
        description: Professor criado com sucesso.
      400:
        description: Dados inválidos.
    """
    return ProfessorController.create_Professor() 

@bp.route('/professores/<int:id>', methods=['PUT'])
def update_a_professor(id):
    """
    Atualiza as informações de um professor existente.
    ---
    tags:
      - Professores
    summary: "Atualiza um professor por ID"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: O ID do professor a ser atualizado.
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            idade:
              type: integer
            materia:
              type: string
            observacoes:
              type: string
    responses:
      200:
        description: Professor atualizado com sucesso.
      404:
        description: Professor não encontrado.
    """
    return ProfessorController.update_Professor(id) 

@bp.route('/professores/<int:id>', methods=['DELETE'])
def delete_a_professor(id):
    """
    Deleta o registro de um professor.
    ---
    tags:
      - Professores
    summary: "Deleta um professor por ID"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: O ID do professor a ser deletado.
    responses:
      204:
        description: "Professor deletado com sucesso (sem conteúdo de retorno)."
      404:
        description: Professor não encontrado.
    """
    return ProfessorController.delete_Professor(id) 

# ========================================================================================
# Rotas das Turmas
# ========================================================================================

@bp.route('/turmas', methods=['GET'])
def get_all_turma():
    """
    Lista todas as turmas cadastradas.
    ---
    tags:
      - Turmas
    summary: "Lista todas as turmas"
    responses:
      200:
        description: Uma lista de todas as turmas.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              descricao:
                type: string
              ativo:
                type: boolean
    """
    return TurmaController.get_all_turma()

@bp.route('/turmas/<int:id>', methods=['GET'])
def get_turma_id(id):
    """
    Busca uma turma específica pelo seu ID.
    ---
    tags:
      - Turmas
    summary: "Busca uma turma por ID"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: O ID único da turma a ser buscada.
    responses:
      200:
        description: Turma encontrada com sucesso.
      404:
        description: Turma não encontrada.
    """
    return TurmaController.get_turma_by_id(id)

@bp.route('/turmas', methods=['POST'])
def create_a_new_turma():
    """
    Cria um novo registro de turma.
    ---
    tags:
      - Turmas
    summary: "Cria uma nova turma"
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - descricao
          properties:
            descricao:
              type: string
              example: "Turma 301 - Período da Manhã"
            professor_id:
              type: integer
              example: 1
            ativo:
              type: boolean
              example: true
    responses:
      201:
        description: Turma criada com sucesso.
      400:
        description: Dados inválidos.
    """
    return TurmaController.create_Turma() 

@bp.route('/turmas/<int:id>', methods=['PUT'])
def update_a_turma(id):
    """
    Atualiza as informações de uma turma existente.
    ---
    tags:
      - Turmas
    summary: "Atualiza uma turma por ID"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: O ID da turma a ser atualizada.
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            descricao:
              type: string
            professor_id:
              type: integer
            ativo:
              type: boolean
    responses:
      200:
        description: Turma atualizada com sucesso.
      404:
        description: Turma não encontrada.
    """
    return TurmaController.update_Turma(id) 

@bp.route('/turmas/<int:id>', methods=['DELETE'])
def delete_a_turma(id):
    """
    Deleta o registro de uma turma.
    ---
    tags:
      - Turmas
    summary: "Deleta uma turma por ID"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: O ID da turma a ser deletada.
    responses:
      204:
        description: "Turma deletada com sucesso (sem conteúdo de retorno)."
      404:
        description: Turma não encontrada.
    """
    return TurmaController.delete_Turma(id) 