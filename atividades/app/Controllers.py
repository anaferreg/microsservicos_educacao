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

        # data_entrega - parse if string
        if 'data_entrega' in data:
            de = data.get('data_entrega')
            if isinstance(de, str):
                try:
                    de = datetime.date.fromisoformat(de)
                except ValueError:
                    return jsonify({'message': 'Formato de data_entrega inválido. Use YYYY-MM-DD.'}), 400
            atividade.data_entrega = de

        # turma/professor validation via gerenciamento if provided
        if 'turma_id' in data:
            turma_id = data.get('turma_id')
            try:
                turma_resp = requests.get(f'http://gerenciamento:5000/turmas/{turma_id}')
                if turma_resp.status_code != 200:
                    return jsonify({'message': 'Turma não encontrada no serviço de gerenciamento'}), 400
            except requests.exceptions.RequestException:
                return jsonify({'message': 'Erro ao conectar com o serviço de gerenciamento'}), 500
            atividade.turma_id = turma_id

        if 'professor_id' in data:
            professor_id = data.get('professor_id')
            try:
                prof_resp = requests.get(f'http://gerenciamento:5000/professores/{professor_id}')
                if prof_resp.status_code != 200:
                    return jsonify({'message': 'Professor não encontrado no serviço de gerenciamento'}), 400
            except requests.exceptions.RequestException:
                return jsonify({'message': 'Erro ao conectar com o serviço de gerenciamento'}), 500
            atividade.professor_id = professor_id

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
        if 'nota' in data:
            notas.nota = data.get('nota', notas.nota)

        if 'atividade_id' in data:
            atividade = Atividade.query.get(data.get('atividade_id'))
            if not atividade:
                return jsonify({'message': 'Atividade não encontrada'}), 400
            notas.atividade_id = data.get('atividade_id')

        if 'aluno_id' in data:
            aluno_id = data.get('aluno_id')
            try:
                aluno_resp = requests.get(f'http://gerenciamento:5000/alunos/{aluno_id}')
                if aluno_resp.status_code != 200:
                    return jsonify({'message': 'Aluno não encontrado no serviço de gerenciamento'}), 400
            except requests.exceptions.RequestException:
                return jsonify({'message': 'Erro ao conectar com o serviço de gerenciamento'}), 500
            notas.aluno_id = aluno_id

        db.session.commit()
        return jsonify(notas.to_json()), 200
