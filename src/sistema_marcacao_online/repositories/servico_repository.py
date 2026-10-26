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