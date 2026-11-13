from flask import Blueprint, render_template , request , session, url_for , redirect
from sistema_marcacao_online.services.servico_servico import listar_servicos
from sistema_marcacao_online.services.marcacao_servico import listar_horarios_disponiveis , criar_marcacao , atualizar_estado_marcacao, listar_marcacoes
from sistema_marcacao_online.services.cliente_servico import obter_ou_registar_cliente
from sistema_marcacao_online.services.administrador_servico import autenticar_administrador
from functools import wraps

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

def administrador_requerido(vista):
    @wraps(vista)
    def funcao_protegida(*args, **kwargs):
        if "id_admin" not in session:
            return redirect(url_for("web.login_admin"))

        return vista(*args, **kwargs)

    return funcao_protegida


@web.route("/admin/login", methods=["GET", "POST"])
def login_admin():
    erro = None

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        palavra_passe = request.form.get("palavra_passe", "")

        id_admin = autenticar_administrador(email, palavra_passe)

        if id_admin is None:
            erro = "Email ou palavra-passe incorretos."
        else:
            session.clear()
            session["id_admin"] = id_admin
            return redirect(url_for("web.painel_admin"))

    return render_template("admin_login.html", erro=erro)

@web.route("/admin", methods=["GET", "POST"])
@administrador_requerido
def painel_admin():
    erro = None
    sucesso = None

    if request.method == "POST":
        try:
            id_marcacao = int(request.form.get("id_marcacao", ""))
        except ValueError:
            erro = "Indique um ID de marcação válido."
        else:
            estado = request.form.get("estado", "")

            try:
                atualizar_estado_marcacao(id_marcacao, estado)
                sucesso = f"Estado da marcação {id_marcacao} atualizado."
            except ValueError as erro_validacao:
                erro = str(erro_validacao)
            except Exception:
                erro = "Não foi possível atualizar a marcação."

    try:
        marcacoes = listar_marcacoes()
    except Exception:
        marcacoes = []
        erro = erro or "Não foi possível carregar as marcações."

    return render_template(
        "admin.html",
        marcacoes=marcacoes,
        erro=erro,
        sucesso=sucesso,
    )

@web.route("/admin/logout", methods=["POST"])
@administrador_requerido
def logout_admin():
    session.clear()
    return redirect(url_for("web.login_admin"))