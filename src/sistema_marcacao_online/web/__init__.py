from flask import Flask


def create_app():
    app = Flask(__name__)

    from sistema_marcacao_online.web.routes import web
    app.register_blueprint(web)

    return app