from flask import Blueprint, jsonify
from .Controllers import ReservaController

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

# =======================================================================
# Rotas das reservas
# =======================================================================

@bp.route('/reservas', methods=['GET'])
def get_all_reserva():
    """
    Lista todas as reservas cadastradas.
    ---
    tags:
      - Reservas
    summary: "Lista todas as reservas"
    responses:
      200:
        description: Uma lista de todas as reservas.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              num_sala:
                type: string
              descricao:
                type: string
              turma_id:
                type: integer
    """
    return ReservaController.get_all_reserva()

@bp.route('/reservas/<int:id>', methods=['GET'])
def get_reserva_by_id(id):
    """
    Busca uma reserva específica pelo seu ID.
    ---
    tags:
      - Reservas
    summary: "Busca uma reserva por ID"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: O ID único da reserva a ser buscada.
    responses:
      200:
        description: Reserva encontrada com sucesso.
        schema:
          type: object
          properties:
            id:
              type: integer
            num_sala:
              type: string
            descricao:
              type: string
            turma_id:
              type: integer
      404:
        description: Reserva não encontrada.
    """
    return ReservaController.get_reserva_by_id(id)

@bp.route('/reservas', methods=['POST'])
def create_reserva():
    """
    Cria uma nova reserva de sala.
    ---
    tags:
      - Reservas
    summary: "Cria uma nova reserva"
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - num_sala
            - turma_id
          properties:
            num_sala:
              type: string
              example: "Sala 101"
            descricao:
              type: string
              example: "Laboratório de Informática"
            turma_id:
              type: integer
              example: 1
    responses:
      201:
        description: Reserva criada com sucesso.
      400:
        description: Dados inválidos ou turma_id inválido.
    """
    return ReservaController.create_Reserva()

@bp.route('/reservas/<int:id>', methods=['PUT'])
def update_reserva(id):
    """
    Atualiza uma reserva existente.
    ---
    tags:
      - Reservas
    summary: "Atualiza uma reserva por ID"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: O ID da reserva a ser atualizada.
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            num_sala:
              type: string
            descricao:
              type: string
            turma_id:
              type: integer
    responses:
      200:
        description: Reserva atualizada com sucesso.
      404:
        description: Reserva não encontrada.
    """
    return ReservaController.update_Reserva(id)

@bp.route('/reservas/<int:id>', methods=['DELETE'])
def delete_reserva(id):
    """
    Remove uma reserva.
    ---
    tags:
      - Reservas
    summary: "Remove uma reserva por ID"
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: O ID da reserva a ser removida.
    responses:
      204:
        description: Reserva removida com sucesso.
      404:
        description: Reserva não encontrada.
    """
    return ReservaController.delete_Reserva(id)