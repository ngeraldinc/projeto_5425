from psycopg.errors import UniqueViolation
from werkzeug.security import check_password_hash, generate_password_hash

from sistema_marcacao_online.repositories.administrador_repositorio import (
    criar_administrador as guardar_administrador,
    obter_administrador_por_email,
)


def criar_administrador(nome: str, email: str, palavra_passe: str) -> int:
    nome_validado = nome.strip() if isinstance(nome, str) else ""
    email_validado = email.strip().lower() if isinstance(email, str) else ""

    if not nome_validado:
        raise ValueError("O nome do administrador é obrigatório.")
    if len(nome_validado) > 100:
        raise ValueError("O nome pode ter no máximo 100 caracteres.")

    if not email_validado or "@" not in email_validado:
        raise ValueError("Indique um email válido.")
    if len(email_validado) > 50:
        raise ValueError("O email pode ter no máximo 50 caracteres.")

    if not isinstance(palavra_passe, str) or len(palavra_passe) < 8:
        raise ValueError("A palavra-passe deve ter pelo menos 8 caracteres.")

    palavra_passe_hash = generate_password_hash(palavra_passe)

    try:
        return guardar_administrador(
            nome_validado,
            email_validado,
            palavra_passe_hash,
        )
    except UniqueViolation as erro:
        raise ValueError("Já existe um administrador com esse email.") from erro


def autenticar_administrador(email: str, palavra_passe: str) -> int | None:
    if not isinstance(email, str) or not isinstance(palavra_passe, str):
        return None

    administrador = obter_administrador_por_email(email.strip().lower())

    if administrador is None:
        return None

    id_admin, _nome, _email, palavra_passe_hash = administrador

    if check_password_hash(palavra_passe_hash, palavra_passe):
        return id_admin

    return None