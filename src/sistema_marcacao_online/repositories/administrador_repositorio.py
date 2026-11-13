from sistema_marcacao_online.database import get_connection


def criar_administrador(nome: str, email: str, palavra_passe_hash: str) -> int:
    with get_connection() as connection:
        resultado = connection.execute(
            """
            INSERT INTO administrador (nome, email, palavra_passe)
            VALUES (%s, %s, %s)
            RETURNING id_admin
            """,
            (nome, email, palavra_passe_hash),
        ).fetchone()

    return resultado[0]


def obter_administrador_por_email(email: str):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT id_admin, nome, email, palavra_passe
            FROM administrador
            WHERE email = %s
            """,
            (email,),
        ).fetchone()