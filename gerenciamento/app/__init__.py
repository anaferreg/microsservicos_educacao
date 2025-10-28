from flask import Flask
from flasgger import Swagger
from .models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///escola.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.config['SWAGGER'] = {
        'title': 'API Escola',
        'uiversion': 3,
        'version': '1.0.0',
        'description': 'Uma API para gerenciar Alunos, Professores e Turmas.'
    }

    swagger = Swagger(app, parse=False)

    from .routes import bp
    app.register_blueprint(bp)

    return app