import logging
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )

    from app.auth.routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
