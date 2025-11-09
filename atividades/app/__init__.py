from flask import Flask
from flasgger import Swagger
from .models import db

def create_app():
    app = Flask(__name__)
    # arquivo de banco específico para o serviço de atividades
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atividades.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.config['SWAGGER'] = {
        'title': 'API Atividades',
        'uiversion': 3,
        'version': '1.0.0',
        'description': 'API para gerenciar Atividades e Notas.'
    }

    swagger = Swagger(app, parse=False)

    from .routes import bp
    app.register_blueprint(bp)

    # garante que as tabelas existam quando o app é inicializado (útil ao usar "flask run")
    with app.app_context():
        db.create_all()

    return app