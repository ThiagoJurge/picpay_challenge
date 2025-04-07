import os
from flask import Flask
from .routes.auth import auth_bp

def create_app(test_config=None):
    app = Flask(__name__)

    from dotenv import load_dotenv
    load_dotenv()

    app.register_blueprint(auth_bp)

    @app.route("/")
    def hello():
        return "Hello, World!"

    return app
