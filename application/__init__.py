import os
from flask import Flask
from .routes.auth import auth_bp
from .routes.teste import teste_bp
from application.models import create_tables  # importa a função que cria as tabelas

def create_app():
    app = Flask(__name__)

    from dotenv import load_dotenv
    load_dotenv()

    app.register_blueprint(auth_bp)
    app.register_blueprint(teste_bp)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    with app.app_context():
        try:
            create_tables()
            print("[INIT] Tabelas verificadas/criadas com sucesso ✅")
        except Exception as e:
            print(f"[ERRO] Ao criar/verificar tabelas: {e}")

    return app
