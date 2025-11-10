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
        num_sala = data.get('num_sala')
        lab = data.get('lab')
        data_value = data.get('data')

        # campos obrigatórios
        if turma_id is None:
            return jsonify({'message': 'O turma_id é obrigatório'}), 400
        if num_sala is None:
            return jsonify({'message': 'O num_sala é obrigatório'}), 400
        if lab is None:
            return jsonify({'message': 'O lab é obrigatório'}), 400
        if data_value is None:
            return jsonify({'message': 'A data é obrigatória'}), 400

        # coerção num_sala -> int
        try:
            num_sala = int(num_sala)
        except (TypeError, ValueError):
            return jsonify({'message': 'num_sala deve ser inteiro'}), 400

        # coerção lab -> bool
        if isinstance(lab, bool):
            pass
        elif isinstance(lab, str):
            if lab.lower() in ['true', 'false']:
                lab = lab.lower() == 'true'
            else:
                return jsonify({'message': 'lab deve ser booleano'}), 400
        else:
            return jsonify({'message': 'lab deve ser booleano'}), 400

        # valida turma via serviço de gerenciamento
        try:
            response = requests.get(f"http://gerenciamento:5000/turmas/{turma_id}")
            if response.status_code != 200:
                return jsonify({'message': 'Turma não encontrada no serviço de gerenciamento'}), 400
        except requests.exceptions.RequestException:
            return jsonify({'message': 'Erro ao conectar com o serviço de gerenciamento'}), 500

        # parsing data
        if isinstance(data_value, str):
            try:
                data_value = datetime.date.fromisoformat(data_value)
            except ValueError:
                return jsonify({'message': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400

        nova_reserva = Reserva(
            num_sala=num_sala,
            lab=lab,
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

        # num_sala (opcional)
        if 'num_sala' in data:
            try:
                reserva.num_sala = int(data.get('num_sala'))
            except (TypeError, ValueError):
                return jsonify({'message': 'num_sala deve ser inteiro'}), 400

        # lab (opcional)
        if 'lab' in data:
            lab = data.get('lab')
            if isinstance(lab, bool):
                reserva.lab = lab
            elif isinstance(lab, str) and lab.lower() in ['true','false']:
                reserva.lab = lab.lower() == 'true'
            else:
                return jsonify({'message': 'lab deve ser booleano'}), 400

        # data (opcional)
        if 'data' in data:
            new_data = data.get('data')
            if isinstance(new_data, str):
                try:
                    new_data = datetime.date.fromisoformat(new_data)
                except ValueError:
                    return jsonify({'message': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400
            reserva.data = new_data

        # turma_id (opcional) -> validar no serviço gerenciamento
        if 'turma_id' in data:
            turma_id = data.get('turma_id')
            try:
                resp = requests.get(f"http://gerenciamento:5000/turmas/{turma_id}")
                if resp.status_code != 200:
                    return jsonify({'message': 'Turma não encontrada no serviço de gerenciamento'}), 400
            except requests.exceptions.RequestException:
                return jsonify({'message': 'Erro ao conectar com o serviço de gerenciamento'}), 500
            reserva.turma_id = turma_id

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