from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reserva(db.Model):
    __tablename__ = 'reservas'

    id = db.Column(db.Integer, primary_key=True)
    num_sala = db.Column(db.Integer, nullable=False)
    lab = db.Column(db.Boolean, nullable=False)
    data = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, nullable=False)
