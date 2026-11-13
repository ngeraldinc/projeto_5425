import os
from dotenv import load_dotenv
from flask import Flask


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

    if not app.config["SECRET_KEY"]:
        raise RuntimeError("Falta FLASK_SECRET_KEY no ficheiro .env.")

    from sistema_marcacao_online.web.routes import web

    app.register_blueprint(web)

    return app