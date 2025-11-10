from datetime import datetime
from flask import request, jsonify
from .models import Aluno, Professor, Turma, db

class AlunoController:
    
    @staticmethod
    def get_all_aluno():
        alunos = Aluno.query.all()
        return jsonify([a.to_json() for a in alunos]), 200

    @staticmethod
    def get_aluno_by_id(id): 
        aluno = Aluno.query.get(id)
        if not aluno:
            return jsonify({'message': 'Aluno não encontrado'}), 404
        
        return jsonify(aluno.to_json()), 200

    @staticmethod
    def create_Aluno(): 
        data = request.json
        nome = data.get('nome')
        
        data_nasciment = None
        if data.get("data_nascimento"):
            try:
                data_nasciment = datetime.strptime(data["data_nascimento"], "%Y-%m-%d").date()
            except ValueError:
                return jsonify({'message': 'Formato de data_nascimento inválido. Use YYYY-MM-DD.'}), 400

        if not nome:
            return jsonify({'message': 'O nome é obrigatório'}), 400

        turma_id = data.get('turma_id')
        if turma_id:
            turma = Turma.query.get(turma_id)
            if not turma:
                return jsonify({'message': 'Turma não encontrada'}), 400

        novo_aluno = Aluno(
            nome=nome,
            idade=data.get('idade'),
            turma_id=turma_id,
            data_nascimento=data_nasciment,
            nota_primeiro_semestre=data.get('nota_primeiro_semestre'),
            nota_segundo_semestre=data.get('nota_segundo_semestre')
        )
        db.session.add(novo_aluno)
        db.session.commit()
        return jsonify(novo_aluno.to_json()), 201
    
    @staticmethod    
    def update_Aluno(id):
        aluno = Aluno.query.get(id)
        if not aluno:
            
            return jsonify({'message': 'Aluno não encontrado'}), 404
        
        data = request.json
        aluno.nome = data.get('nome', aluno.nome)
        aluno.idade = data.get('idade', aluno.idade)

        turma_id = data.get('turma_id')
        if turma_id:
            turma = Turma.query.get(turma_id)
            if not turma:
                return jsonify({'message': 'Turma não encontrada'}), 400
            aluno.turma_id = turma_id

        # data_nascimento parsing if string provided
        if 'data_nascimento' in data:
            dn = data.get('data_nascimento')
            if isinstance(dn, str):
                try:
                    dn = datetime.strptime(dn, "%Y-%m-%d").date()
                except ValueError:
                    return jsonify({'message': 'Formato de data_nascimento inválido. Use YYYY-MM-DD.'}), 400
            aluno.data_nascimento = dn
        
        aluno.nota_primeiro_semestre = data.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre)
        aluno.nota_segundo_semestre = data.get('nota_segundo_semestre', aluno.nota_segundo_semestre)
        
        db.session.commit()
        return jsonify(aluno.to_json()), 200
    
    @staticmethod
    def delete_Aluno(id):
        aluno = Aluno.query.get(id)
        
        if not aluno:
            
            return jsonify({'message': 'Aluno não encontrado'}), 404
        
        db.session.delete(aluno)
        db.session.commit()
        
        return '', 204
    

class ProfessorController:
    
    @staticmethod
    def get_all_professor():
        
        professores = Professor.query.all()
        
        return jsonify([p.to_json() for p in professores]), 200

    @staticmethod
    def get_professor_by_id(id):
        professor = Professor.query.get(id)
        
        if not professor:
            return jsonify({'message': 'Professor não encontrado'}), 404
        
        return jsonify(professor.to_json()), 200

    @staticmethod
    def create_Professor():
        data = request.json
        nome = data.get('nome')
    
        if not nome:
            return jsonify({'message': 'O nome é obrigatório'}), 400

        novo_professor = Professor(
            nome=nome,
            idade=data.get('idade'),
            materia=data.get('materia'),
            observacoes=data.get('observacoes')
        )
        db.session.add(novo_professor)
        db.session.commit()
        return jsonify(novo_professor.to_json()), 201
    
    @staticmethod    
    def update_Professor(id):
        professor = Professor.query.get(id)
        if not professor:
            
            return jsonify({'message': 'Professor não Encontrado'}), 404
        
        data = request.json
        professor.nome = data.get('nome', professor.nome)
        professor.idade = data.get('idade', professor.idade)
        professor.materia = data.get('materia', professor.materia)
        professor.observacoes = data.get('observacoes', professor.observacoes)
        
        db.session.commit()
        return jsonify(professor.to_json()), 200
    
    @staticmethod
    def delete_Professor(id):

        professor = Professor.query.get(id)

        if not professor:
            return jsonify({'message': 'Professor Não Encontrado'}), 404
        

        db.session.delete(professor)
        db.session.commit()
        
        return '', 204
    

class TurmaController:
    
    @staticmethod
    def get_all_turma():
        turmas = Turma.query.all()
        return jsonify([t.to_json() for t in turmas]), 200

    @staticmethod
    def get_turma_by_id(id): 
        turma = Turma.query.get(id)
        if not turma:
            return jsonify({'message': 'Turma não encontrada'}), 404
        
        return jsonify(turma.to_json()), 200

    @staticmethod
    def create_Turma(): 
        data = request.json

        descricao = data.get('descricao')
        professor_id = data.get('professor_id')
    
        if not descricao:
            return jsonify({'message': 'A descrição é obrigatória'}), 400

        if professor_id:
            professor = Professor.query.get(professor_id)
            if not professor:
                return jsonify({'message': 'Professor não encontrado'}), 400

        nova_turma = Turma(
            descricao=descricao,
            professor_id=professor_id,
            ativo=data.get('ativo', True) 
        )
        db.session.add(nova_turma)
        db.session.commit()
        return jsonify(nova_turma.to_json()), 201
    
    @staticmethod    
    def update_Turma(id):
        turma = Turma.query.get(id)
        if not turma:
    
            return jsonify({'message': 'Turma não encontrada'}), 404
        
        data = request.json
        
        professor_id = data.get('professor_id')
        if professor_id:
            professor = Professor.query.get(professor_id)
            if not professor:
                return jsonify({'message': 'Professor não encontrado'}), 400
        
        turma.descricao = data.get('descricao', turma.descricao)
        turma.professor_id = professor_id if professor_id else turma.professor_id
        turma.ativo = data.get('ativo', turma.ativo)
        
        db.session.commit()
        return jsonify(turma.to_json()), 200
    
    @staticmethod
    def delete_Turma(id):
        turma = Turma.query.get(id)
        
        if not turma:
            
            return jsonify({'message':'Turma não encontrada'}), 404
        
        db.session.delete(turma)
        db.session.commit()
        
        return '', 204