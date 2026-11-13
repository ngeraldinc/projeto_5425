from flask import Blueprint, render_template

from sistema_marcacao_online.services.servico_servico import listar_servicos

web = Blueprint("web", __name__)


@web.route("/")
def inicio():
    servicos = listar_servicos()
    return render_template("servicos.html", servicos=servicos)