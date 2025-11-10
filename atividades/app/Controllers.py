import requests
import datetime
from flask import request, jsonify
from .models import Atividade, Nota, db

class AtividadesController:
    @staticmethod
    def get_all_atividades():
        atividades = Atividade .query.all()
        return jsonify([r.to_json() for r in atividades]), 200

    @staticmethod
    def get_atividade_by_id(id):
        atividade = Atividade.query.get(id)
        if not atividade:
            return jsonify({'message': 'Atividade não encontrada'}), 404
        return jsonify(atividade.to_json()), 200

    @staticmethod
    def create_Atividade():
        data = request.json
        nome_atividade = data.get('nome_atividade')
        peso_porcento = data.get('peso_porcento')
        turma_id = data.get('turma_id')
        professor_id = data.get('professor_id')
        data_entrega_str = data.get('data_entrega')

        if not nome_atividade or peso_porcento is None or not turma_id or not professor_id or not data_entrega_str:
            return jsonify({'message': 'Campos obrigatórios ausentes'}), 400

        try:
            data_entrega = datetime.date.fromisoformat(data_entrega_str)
        except ValueError:
            return jsonify({'message': 'Formato de data inválido'}), 400

        try:
            turma_resp = requests.get(f'http://gerenciamento:5000/turmas/{turma_id}')
            if turma_resp.status_code != 200:
                return jsonify({'message': 'Turma não encontrada no serviço de gerenciamento'}), 400
            prof_resp = requests.get(f'http://gerenciamento:5000/professores/{professor_id}')
            if prof_resp.status_code != 200:
                return jsonify({'message': 'Professor não encontrado no serviço de gerenciamento'}), 400
        except requests.exceptions.RequestException:
            return jsonify({'message': 'Erro ao conectar com o serviço de gerenciamento'}), 500

        nova_atividade = Atividade(
            nome_atividade=nome_atividade,
            descricao=data.get('descricao'),
            peso_porcento=peso_porcento,
            data_entrega=data_entrega,
            turma_id=turma_id,
            professor_id=professor_id
        )
        db.session.add(nova_atividade)
        db.session.commit()
        return jsonify(nova_atividade.to_json()), 201

    @staticmethod    
    def update_atividade(id):
        atividade = Atividade.query.get(id)
        if not atividade:
            return jsonify({'message': 'Atividade não encontrada'}), 404

        data = request.json
        atividade.nome_atividade = data.get('nome_atividade', atividade.nome_atividade)
        atividade.descricao = data.get('descricao', atividade.descricao)
        atividade.peso_porcento = data.get('peso_porcento', atividade.peso_porcento)
        atividade.data_entrega = data.get('data_entrega', atividade.data_entrega)
        atividade.turma_id = data.get('turma_id', atividade.turma_id)
        atividade.professor_id = data.get('professor_id', atividade.professor_id)

        db.session.commit()
        return jsonify(atividade.to_json()), 200

    @staticmethod
    def delete_atividade(id):
        atividade = Atividade.query.get(id)
        if not atividade:
            return jsonify({'message': 'Atividade não encontrada'}), 404
        db.session.delete(atividade)
        db.session.commit()
        return '', 204


class NotasController:
    @staticmethod
    def get_all_notas():
        notas = Nota.query.all()
        return jsonify([r.to_json() for r in notas]), 200

    @staticmethod
    def get_notas_by_id(id):
        notas = Nota.query.get(id)
        if not notas:
            return jsonify({'message': 'Nota não encontrada'}), 404
        return jsonify(notas.to_json()), 200

    @staticmethod
    def create_Notas():
        data = request.json
        aluno_id = data.get('aluno_id')
        atividade_id = data.get('atividade_id')
        nota_valor = data.get('nota')

        if not aluno_id or not atividade_id or nota_valor is None:
            return jsonify({'message': 'Campos obrigatórios ausentes'}), 400

        try:
            aluno_resp = requests.get(f'http://gerenciamento:5000/alunos/{aluno_id}')
            if aluno_resp.status_code != 200:
                return jsonify({'message': 'Aluno não encontrado no serviço de gerenciamento'}), 400
        except requests.exceptions.RequestException:
            return jsonify({'message': 'Erro ao conectar com o serviço de gerenciamento'}), 500

        atividade = Atividade.query.get(atividade_id)
        if not atividade:
            return jsonify({'message': 'Atividade não encontrada'}), 400

        nova_nota = Nota(
            nota=nota_valor,
            atividade_id=atividade_id,
            aluno_id=aluno_id
        )
        db.session.add(nova_nota)
        db.session.commit()
        return jsonify(nova_nota.to_json()), 201

    @staticmethod
    def update_Notas(id):
        notas = Nota.query.get(id)
        if not notas:
            return jsonify({'message': 'Nota não encontrada'}), 404

        data = request.json
        notas.nota = data.get('nota', notas.nota)
        notas.atividade_id = data.get('atividade_id', notas.atividade_id)
        notas.aluno_id = data.get('aluno_id', notas.aluno_id)
        db.session.commit()
        return jsonify(notas.to_json()), 200

    @staticmethod
    def delete_Notas(id):
        notas = Nota.query.get(id)
        if not notas:
            return jsonify({'message': 'Nota não encontrada'}), 404
        db.session.delete(notas)
        db.session.commit()
        return '', 204
