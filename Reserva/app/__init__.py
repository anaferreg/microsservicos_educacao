from flask import Flask
from flasgger import Swagger
from .models import db

def create_app():
    app = Flask(__name__)
    # arquivo de banco específico para o serviço de reservas
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.config['SWAGGER'] = {
        'title': 'API Reservas',
        'uiversion': 3,
        'version': '1.0.0',
        'description': 'API para gerenciar Reservas.'
    }

    swagger = Swagger(app, parse=False)

    from .routes import bp
    app.register_blueprint(bp)

    return app