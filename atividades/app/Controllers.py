from flask import request, jsonify
from .models import Atividades,Notas,db

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
        
    def create_Atividade():
        data=request.json
        turma_id=data.get('turma_id')
        professor_id=data.get('professor_id')
        if not turma_id:
            return jsonify({'message': 'O turma_id é obrigatório'}), 400
        if not professor_id:
            return jsonify({'message': 'O professor_id é obrigatório'}), 400
        nova_atividade=Atividades(
            nome_atividade=data.get('num_sala'),
            descricao=data.get('descricao'),
            peso_porcento=data.get('peso_porcento'),
            data_entrega=data.get('data_entrega'),
            turma_id=turma_id,
            professor_id=professor_id
        )
        
        
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