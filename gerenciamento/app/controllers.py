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
    
        if not nome:
            return jsonify({'message': 'O nome é obrigatório'}), 400

        novo_aluno = Aluno(
            nome=nome,
            idade=data.get('idade'),
            turma_id=data.get('turma_id'),
            data_nascimento=data.get('data_nascimento'),
            
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
        aluno.turma_id = data.get('turma_id', aluno.turma_id)
        aluno.data_nascimento = data.get('data_nascimento', aluno.data_nascimento)
        
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
    
        if not descricao:
        
            return jsonify({'message': 'A descrição é obrigatória'}), 400

       
        nova_turma = Turma(
            descricao=descricao,
  
            professor_id=data.get('professor_id'),
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
        
       
        turma.descricao = data.get('descricao', turma.descricao)
        turma.professor_id = data.get('professor_id', turma.professor_id)
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