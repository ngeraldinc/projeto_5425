from datetime import date, datetime, time
from psycopg.errors import UniqueViolation
from sistema_marcacao_online.repositories.marcacao_repositorio import (contar_faltas_cliente, criar_marcacao as criar_marcacao_repo,
horario_disponivel, atualizar_estado_marcacao as atualizar_estado_marcacao_repo, listar_marcacoes as listar_marcacoes_repo,
listar_horarios_ocupados as listar_horarios_ocupados_repo)
from sistema_marcacao_online.repositories.servico_repositorio import listar_servicos as listar_servicos_repo

def _validar_data(valor: str | date) -> date:
    try:
        data_validada = (
            date.fromisoformat(valor.strip())
            if isinstance(valor, str)
            else valor
        )
    except ValueError:
        raise ValueError("A data deve estar no formato AAAA-MM-DD.")

    if not isinstance(data_validada, date) or isinstance(data_validada, datetime):
        raise ValueError("A data indicada não é válida.")

    if data_validada < date.today():
        raise ValueError("A data da marcação não pode estar no passado.")

    return data_validada

def _validar_hora(valor: str | time) -> time:
    if isinstance(valor, str):
        texto = valor.strip()

        try:
            if len(texto) != 5 or texto[2] != ":":
                raise ValueError

            hora_validada = time.fromisoformat(texto)
        except ValueError:
            raise ValueError(
                "A hora deve estar no formato HH:MM, por exemplo 14:30."
            )
    elif isinstance(valor, time):
        hora_validada = valor
    else:
        raise ValueError("A hora indicada não é válida.")

    return hora_validada

def _validar_ids_servicos(valores: str | list[int]) -> list[int]:
    try:
        partes = valores.split(",") if isinstance(valores, str) else valores
        ids = [int(valor) for valor in partes]
    except (ValueError, TypeError):
        raise ValueError("Indique os IDs dos serviços, separados por vírgulas.")

    if not ids:
        raise ValueError("Selecione pelo menos um serviço.")

    if any(id_servico <= 0 for id_servico in ids):
        raise ValueError("Os IDs dos serviços devem ser números positivos.")

    if len(ids) != len(set(ids)):
        raise ValueError("Não indique o mesmo serviço mais de uma vez.")

    ids_existentes = {
        servico[0] for servico in listar_servicos_repo()
    }
    ids_invalidos = [id_servico for id_servico in ids if id_servico not in ids_existentes]

    if ids_invalidos:
        raise ValueError(f"Não existem serviços com estes IDs: {ids_invalidos}.")

    return ids

def criar_marcacao(
    id_cliente: int,
    data: str | date,
    hora: str | time,
    ids_servicos: str | list[int],
) -> int:
    if id_cliente <= 0:
        raise ValueError("O ID do cliente deve ser um número positivo.")

    data_validada = _validar_data(data)
    hora_validada = _validar_hora(hora)
    ids_validos = _validar_ids_servicos(ids_servicos)

    if data_validada.weekday() >= 5:
        raise ValueError("Só é possível marcar de segunda a sexta-feira.")
    
    horarios_permitidos = [time(hora) for hora in range(8, 20, 2)]
    
    if hora_validada not in horarios_permitidos:
        raise ValueError(
        "Escolha um horário de duas em duas horas, "
        "entre as 08:00 e as 18:00."
        )

    faltas = contar_faltas_cliente(id_cliente)
    if faltas >= 2:
        raise ValueError(
            "Não é possível criar a marcação: o cliente tem duas ou mais faltas. "
            "Deve contactar a administração por WhatsApp."
        )

    if not horario_disponivel(data_validada, hora_validada):
        raise ValueError("Esse horário já está ocupado. Escolha outro.")

    try:
        return criar_marcacao_repo(
            id_cliente,
            data_validada,
            hora_validada,
            ids_validos,
        )
    except UniqueViolation as erro:
        raise ValueError(
            "Esse horário acabou de ser reservado. Escolha outro."
        ) from erro

def listar_marcacoes():
    return listar_marcacoes_repo()

def atualizar_estado_marcacao(id_marcacao: int, estado: str) -> int:
    if id_marcacao <= 0:
        raise ValueError("O ID da marcação deve ser um número positivo.")

    if not isinstance(estado, str):
        raise ValueError("O estado indicado não é válido.")

    estado_validado = estado.strip().lower()
    estados_permitidos = {"realizada", "cancelada", "falta"}

    if estado_validado not in estados_permitidos:
        raise ValueError(
            "O estado deve ser realizada, cancelada ou falta."
        )

    id_atualizado = atualizar_estado_marcacao_repo(
        id_marcacao,
        estado_validado,
    )

    if id_atualizado is None:
        raise ValueError(f"Não existe uma marcação com o ID {id_marcacao}.")

    return id_atualizado

def listar_horarios_disponiveis(data: str | date) -> list[time]:
    data_validada = _validar_data(data)

    if data_validada.weekday() >= 5:
        raise ValueError("Só é possível marcar de segunda a sexta-feira.")

    horarios_do_dia = [time(hora) for hora in range(8, 20, 2)]
    horarios_ocupados = set(
        listar_horarios_ocupados_repo(data_validada)
    )

    return [
        hora
        for hora in horarios_do_dia
        if hora not in horarios_ocupados
    ]