from flask import Blueprint, render_template , request
from sistema_marcacao_online.services.servico_servico import listar_servicos
from sistema_marcacao_online.services.marcacao_servico import listar_horarios_disponiveis , criar_marcacao
from sistema_marcacao_online.services.cliente_servico import obter_ou_registar_cliente

web = Blueprint("web", __name__)


@web.route("/")
def inicio():
    servicos = listar_servicos()
    return render_template("servicos.html", servicos=servicos)

@web.route("/marcacao/nova", methods=["GET", "POST"])
def nova_marcacao():
    servicos = listar_servicos()
    horarios = []
    erro = None
    sucesso = None

    if request.method == "POST":
        data = request.form.get("data", "").strip()
        hora = request.form.get("hora", "").strip()
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()
        ids_servicos = request.form.getlist("ids_servicos")

        try:
            horarios_disponiveis = listar_horarios_disponiveis(data)
            horas_validas = {
                horario.strftime("%H:%M")
                for horario in horarios_disponiveis
            }

            if hora not in horas_validas:
                raise ValueError("Escolha um horário que esteja disponível.")

            ids_existentes = {str(servico[0]) for servico in servicos}

            if not ids_servicos:
                raise ValueError("Selecione pelo menos um serviço.")

            if any(id_servico not in ids_existentes for id_servico in ids_servicos):
                raise ValueError("Um dos serviços selecionados não existe.")

            if len(ids_servicos) != len(set(ids_servicos)):
                raise ValueError("Não selecione o mesmo serviço mais de uma vez.")

            id_cliente = obter_ou_registar_cliente(nome, telefone, email)
            id_marcacao = criar_marcacao(
                id_cliente,
                data,
                hora,
                ids_servicos,
            )
            sucesso = f"Marcação criada com sucesso. ID: {id_marcacao}"

        except ValueError as erro_validacao:
            erro = str(erro_validacao)
        except Exception:
            erro = "Não foi possível criar a marcação. Verifique os dados e tente novamente."

        data_selecionada = data
    else:
        data_selecionada = request.args.get("data", "").strip()

    if data_selecionada:
        try:
            horarios = listar_horarios_disponiveis(data_selecionada)
        except ValueError as erro_validacao:
            if erro is None:
                erro = str(erro_validacao)

    return render_template(
        "marcacao_form.html",
        data=data_selecionada,
        horarios=horarios,
        servicos=servicos,
        erro=erro,
        sucesso=sucesso,
    )