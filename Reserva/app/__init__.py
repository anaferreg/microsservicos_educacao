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

    swagger = Swagger(app, config={
        'headers': [],
        'specs': [
            {
                'endpoint': 'swagger',
                'route': '/swagger.json',
                'rule_filter': lambda rule: True,  # inclui todas as rotas
                'model_filter': lambda tag: True,  # inclui todos os modelos
            }
        ],
        'static_url_path': '/flasgger_static',
        'swagger_ui': True,
        'specs_route': '/swagger/'  # 👈 muda a UI para /swagger
    })

    from .routes import bp
    app.register_blueprint(bp)

    # garante que as tabelas existam quando o app é inicializado (útil ao usar "flask run")
    with app.app_context():
        db.create_all()

    return app