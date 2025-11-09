from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reserva(db.Model):
    __tablename__ = 'reservas'

    id = db.Column(db.Integer, primary_key=True)
    num_sala = db.Column(db.Integer, nullable=False)
    lab = db.Column(db.Boolean, nullable=False)
    data = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'num_sala': self.num_sala,
            'lab': self.lab,
            'data': self.data.isoformat() if self.data else None,
            'turma_id': self.turma_id
        }
