from sistema_marcacao_online.database import get_connection
from decimal import Decimal
from sistema_marcacao_online.database import get_connection


def listar_servicos():
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT id_servico, nome, descricao, preco
            FROM servico
            ORDER BY nome
            """
        ).fetchall()

def registar_servico(nome: str, descricao: str, preco: Decimal) -> int:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO servico (nome, descricao, preco)
                VALUES (%s, %s, %s)
                RETURNING id_servico
                """,
                (nome, descricao, preco),
            )
            resultado = cursor.fetchone()

        return resultado[0]