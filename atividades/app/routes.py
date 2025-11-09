from flask import Blueprint, jsonify
from .Controllers import AtividadesController, NotasController

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
# Rotas das atividades
# =======================================================================

@bp.route('/atividades', methods=['GET'])
def get_all_atividades():
        """
        Lista todas as atividades cadastradas.
        ---
        tags:
            - Atividades
        summary: "Lista todas as atividades"
        responses:
            200:
                description: Uma lista de todas as atividades.
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
                            nome_atividade:
                                type: string
                            descricao:
                                type: string
                            data:
                                type: string
                                format: date
                            turma_id:
                                type: integer
                            professor_id:
                                type: integer
        """
        return AtividadesController.get_all_atividades()

@bp.route('/atividades/<int:id>', methods=['GET'])
def get_atividade_id(id):
        """
        Busca uma atividade específica pelo seu ID.
        ---
        tags:
            - Atividades
        summary: "Busca uma atividade por ID"
        parameters:
            - in: path
                name: id
                type: integer
                required: true
                description: O ID único da atividade a ser buscada.
        responses:
            200:
                description: Atividade encontrada com sucesso.
            404:
                description: Atividade não encontrada.
        """
        return AtividadesController.get_atividade_by_id(id)

@bp.route('/atividades', methods=['POST'])
def create_atividade():
        """
        Cria uma nova atividade.
        ---
        tags:
            - Atividades
        summary: "Cria uma nova atividade"
        parameters:
            - in: body
                name: body
                required: true
                schema:
                    type: object
                    required:
                        - nome_atividade
                        - turma_id
                        - professor_id
                    properties:
                        nome_atividade:
                            type: string
                            example: "Projeto Final de Python"
                        descricao:
                            type: string
                            example: "Desenvolver uma API REST com Flask"
                        data:
                            type: string
                            format: date
                            example: "2025-12-01"
                        turma_id:
                            type: integer
                            example: 1
                        professor_id:
                            type: integer
                            example: 1
        responses:
            201:
                description: Atividade criada com sucesso.
            400:
                description: Dados inválidos ou IDs de turma/professor inválidos.
        """
        return AtividadesController.create_Atividade()

@bp.route('/atividades/<int:id>', methods=['PUT'])
def update_atividade(id):
        """
        Atualiza uma atividade existente.
        ---
        tags:
            - Atividades
        summary: "Atualiza uma atividade por ID"
        parameters:
            - in: path
                name: id
                type: integer
                required: true
                description: O ID da atividade a ser atualizada.
            - in: body
                name: body
                required: true
                schema:
                    type: object
                    properties:
                        nome_atividade:
                            type: string
                        descricao:
                            type: string
                        data:
                            type: string
                            format: date
                        turma_id:
                            type: integer
                        professor_id:
                            type: integer
        responses:
            200:
                description: Atividade atualizada com sucesso.
            404:
                description: Atividade não encontrada.
        """
        return AtividadesController.update_atividade(id)

@bp.route('/atividades/<int:id>', methods=['DELETE'])
def delete_atividade(id):
        """
        Remove uma atividade.
        ---
        tags:
            - Atividades
        summary: "Remove uma atividade por ID"
        parameters:
            - in: path
                name: id
                type: integer
                required: true
                description: O ID da atividade a ser removida.
        responses:
            204:
                description: Atividade removida com sucesso.
            404:
                description: Atividade não encontrada.
        """
        return AtividadesController.delete_atividade(id)

# =======================================================================
# Rotas das notas
# =======================================================================

@bp.route('/notas', methods=['GET'])
def get_all_notas():
        """
        Lista todas as notas cadastradas.
        ---
        tags:
            - Notas
        summary: "Lista todas as notas"
        responses:
            200:
                description: Uma lista de todas as notas.
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
                            aluno_id:
                                type: integer
                            atividade_id:
                                type: integer
                            nota:
                                type: number
                                format: float
                            data_entrega:
                                type: string
                                format: date
        """
        return NotasController.get_all_notas()

@bp.route('/notas/<int:id>', methods=['GET'])
def get_notas_id(id):
        """
        Busca uma nota específica pelo seu ID.
        ---
        tags:
            - Notas
        summary: "Busca uma nota por ID"
        parameters:
            - in: path
                name: id
                type: integer
                required: true
                description: O ID único da nota a ser buscada.
        responses:
            200:
                description: Nota encontrada com sucesso.
            404:
                description: Nota não encontrada.
        """
        return NotasController.get_notas_by_id(id)

@bp.route('/notas', methods=['POST'])
def create_notas():
        """
        Registra uma nova nota.
        ---
        tags:
            - Notas
        summary: "Registra uma nova nota"
        parameters:
            - in: body
                name: body
                required: true
                schema:
                    type: object
                    required:
                        - aluno_id
                        - atividade_id
                        - nota
                    properties:
                        aluno_id:
                            type: integer
                            example: 1
                        atividade_id:
                            type: integer
                            example: 1
                        nota:
                            type: number
                            format: float
                            example: 8.5
                        data_entrega:
                            type: string
                            format: date
                            example: "2025-11-30"
        responses:
            201:
                description: Nota registrada com sucesso.
            400:
                description: Dados inválidos ou IDs de aluno/atividade inválidos.
        """
        return NotasController.create_Notas()

@bp.route('/notas/<int:id>', methods=['PUT'])
def update_notas(id):
        """
        Atualiza uma nota existente.
        ---
        tags:
            - Notas
        summary: "Atualiza uma nota por ID"
        parameters:
            - in: path
                name: id
                type: integer
                required: true
                description: O ID da nota a ser atualizada.
            - in: body
                name: body
                required: true
                schema:
                    type: object
                    properties:
                        nota:
                            type: number
                            format: float
                        data_entrega:
                            type: string
                            format: date
        responses:
            200:
                description: Nota atualizada com sucesso.
            404:
                description: Nota não encontrada.
        """
        return NotasController.update_Notas(id)

@bp.route('/notas/<int:id>', methods=['DELETE'])
def delete_notas(id):
        """
        Remove uma nota.
        ---
        tags:
            - Notas
        summary: "Remove uma nota por ID"
        parameters:
            - in: path
                name: id
                type: integer
                required: true
                description: O ID da nota a ser removida.
        responses:
            204:
                description: Nota removida com sucesso.
            404:
                description: Nota não encontrada.
        """
        return NotasController.delete_Notas(id)