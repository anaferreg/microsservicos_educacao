from flask import request, jsonify
from .models import Atividades,Notas,db
import datetime

class AtividadesController:
    
    @staticmethod
    def get_all_atividades():
        atividades=Atividades.query.all()
        
        return jsonify([r.to_json() for r in atividades]), 200

    @staticmethod
    def get_atividade_by_id(id):
        atividades=Atividades.query.get(id)
        if not atividades:
            return jsonify({'message':'Atividades não'})
        
    @staticmethod
    def create_Atividade():
        data = request.json
        if data is None:
            return jsonify({'message': 'Nenhum JSON recebido ou formato inválido.'}), 400
        
        # validar campos obrigatórios
        nome_atividade = data.get('nome_atividade')
        peso_porcento = data.get('peso_porcento')
        turma_id = data.get('turma_id')
        professor_id = data.get('professor_id')
        data_entrega_str = data.get('data_entrega')
        
        if not nome_atividade:
            return jsonify({'message': 'O nome_atividade é obrigatório'}), 400
        if peso_porcento is None:
            return jsonify({'message': 'O peso_porcento é obrigatório'}), 400
        if not turma_id:
            return jsonify({'message': 'O turma_id é obrigatório'}), 400
        if not professor_id:
            return jsonify({'message': 'O professor_id é obrigatório'}), 400
        if not data_entrega_str:
            return jsonify({'message': 'A data_entrega é obrigatória'}), 400
            
        # converter string de data para objeto Date
        try:
            data_entrega = datetime.date.fromisoformat(data_entrega_str)
        except ValueError:
            return jsonify({'message': 'Formato de data inválido. Use YYYY-MM-DD'}), 400

        nova_atividade = Atividades(
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
        atividade = Atividades.query.get(id)
        if not atividade:
            return jsonify({'message': 'Atividade não encontrada'}), 404
        
        data = request.json
        
        # Atualiza apenas os campos enviados, mantém os valores existentes se não enviados
        atividade.nome_atividade = data.get('nome_atividade', atividade.nome_atividade)
        atividade.descricao = data.get('descricao', atividade.descricao)
        atividade.data_entrega = data.get('data_entrega', atividade.data_entrega)
        atividade.turma_id = data.get('turma_id', atividade.turma_id)
        atividade.professor_id = data.get('professor_id', atividade.professor_id)
        
        db.session.commit()
        return jsonify(atividade.to_json()), 200

    @staticmethod
    def delete_atividade(id):
        atividade = Atividades.query.get(id)
        
        if not atividade:
            return jsonify({'message': 'Atividade não encontrada'}), 404
        
        db.session.delete(atividade)
        db.session.commit()
        
        return '', 204
        
class NotasController:
    
    @staticmethod
    def get_all_notas():
        notas=Notas.query.all()
        
        return jsonify([r.to_json() for r in notas]), 200
    
    @staticmethod
    def get_notas_by_id(id):
        notas=Notas.query.get(id)
        if not notas:
            return jsonify({'message': 'Notas não encontrado'}), 404
    
    @staticmethod
    def create_Notas():
        data=request.json
        aluno_id=data.get('aluno_id')
        atividade_id=data.get('atividade_id')
        #Precisa  sincronizar com o ID de uma Aluno e Atividade
        # serviço de Gerenciamento (ex: GET /Aluno/<Aluno_id>)
        
        if not aluno_id:
            return jsonify({'message': 'O turma_id é obrigatório'}), 400
        nova_notas=Notas(
        nota=data.get('nota'),
        atividade_id=atividade_id,
        aluno_id=aluno_id
    )
        db.session.add(nova_notas)
        db.session.commit()
        return jsonify(nova_notas.to_json()), 201
    
    @staticmethod
    def update_Notas(id):
        notas=Notas.query.get(id)
        
        if not notas:
            return jsonify({'message': 'Notas é obrigatório'}), 400
        
        data = request.json
        notas.nova_notas = data.get('nova_notas', notas.nova_notas)
        notas.atividade_id = data.get('atividade_id', notas.atividade_id)
        notas.aluno_id = data.get('aluno_id', notas.aluno_id)
        
        db.session.commit()
        return jsonify(notas.to_json()), 200
    
    @staticmethod
    def delete_Notas(id):
        notas = Notas.query.get(id)
        if not notas:
            return jsonify({'message': 'Notas não encontrada'}), 404
        
        db.session.delete(notas)
        db.session.commit()
        return '', 204