from flask import request, jsonify
from models import Reserva,db
#
class ReservaController:
    
    @staticmethod
    def get_all_reserva():
        reservas=Reserva.query.all()
        
        return jsonify([r.to_json() for r in reservas]), 200
    
    @staticmethod
    def get_reserva_by_id(id):
        reserva=Reserva.query.get(id)
        if not reserva:
            return jsonify({'message': 'Reserva não encontrado'}), 404
    
    @staticmethod
    def create_Reserva():
        data=request.json
        turma_id=data.get('turma_id')
        #Precisa  sincronizar com o ID de uma turma
        # serviço de Gerenciamento (ex: GET /turmas/<turma_id>)
        
        if not turma_id:
            return jsonify({'message': 'O turma_id é obrigatório'}), 400
        nova_reserva=Reserva(
        num_sala=data.get('num_sala'),
        lab=data.get('lab'),
        data=data.get('data'),
        turma_id=turma_id
    )
        db.session.add(nova_reserva)
        db.session.commit()
        return jsonify(nova_reserva.to_json()), 201
    
    @staticmethod
    def update_Reserva(id):
        reserva=Reserva.query.get(id)
        
        if not reserva:
            return jsonify({'message': 'Reserva é obrigatório'}), 400
        
        data = request.json
        reserva.num_sala = data.get('num_sala', reserva.num_sala)
        reserva.lab = data.get('lab', reserva.lab)
        reserva.data = data.get('data', reserva.data) # Adicionar conversão
        reserva.turma_id = data.get('turma_id', reserva.turma_id)
        
        db.session.commit()
        return jsonify(reserva.to_json()), 200
    
    @staticmethod
    def delete_Reserva(id):
        reserva = Reserva.query.get(id)
        if not reserva:
            return jsonify({'message': 'Reserva não encontrada'}), 404
        
        db.session.delete(reserva)
        db.session.commit()
        return '', 204