from flask import request, jsonify
from .models import Reserva, db
import datetime
import requests

class ReservaController:
    
    @staticmethod
    def get_all_reserva():
        reservas = Reserva.query.all()
        return jsonify([r.to_json() for r in reservas]), 200
    
    @staticmethod
    def get_reserva_by_id(id):
        reserva = Reserva.query.get(id)
        if not reserva:
            return jsonify({'message': 'Reserva não encontrada'}), 404
        return jsonify(reserva.to_json()), 200
    
    @staticmethod
    def create_reserva():
        data = request.json
        turma_id = data.get('turma_id')

        if not turma_id:
            return jsonify({'message': 'O turma_id é obrigatório'}), 400

        try:
            response = requests.get(f"http://gerenciamento:5000/turmas/{turma_id}")
            if response.status_code != 200:
                return jsonify({'message': 'Turma não encontrada no serviço de gerenciamento'}), 400
        except requests.exceptions.RequestException:
            return jsonify({'message': 'Erro ao conectar com o serviço de gerenciamento'}), 500

        data_value = data.get('data')
        if isinstance(data_value, str):
            try:
                data_value = datetime.date.fromisoformat(data_value)
            except ValueError:
                return jsonify({'message': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400

        nova_reserva = Reserva(
            num_sala=data.get('num_sala'),
            lab=data.get('lab'),
            data=data_value,
            turma_id=turma_id
        )
        db.session.add(nova_reserva)
        db.session.commit()
        return jsonify(nova_reserva.to_json()), 201
    
    @staticmethod
    def update_reserva(id):
        reserva = Reserva.query.get(id)
        
        if not reserva:
            return jsonify({'message': 'Reserva não encontrada'}), 404
        
        data = request.json
        reserva.num_sala = data.get('num_sala', reserva.num_sala)
        reserva.lab = data.get('lab', reserva.lab)

        new_data = data.get('data', reserva.data)
        if isinstance(new_data, str):
            try:
                new_data = datetime.date.fromisoformat(new_data)
            except ValueError:
                return jsonify({'message': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400
        reserva.data = new_data

        reserva.turma_id = data.get('turma_id', reserva.turma_id)
        
        db.session.commit()
        return jsonify(reserva.to_json()), 200
    
    @staticmethod
    def delete_reserva(id):
        reserva = Reserva.query.get(id)
        if not reserva:
            return jsonify({'message': 'Reserva não encontrada'}), 404
        
        db.session.delete(reserva)
        db.session.commit()
        return '', 204