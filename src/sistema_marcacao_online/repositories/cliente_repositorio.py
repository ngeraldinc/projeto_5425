from sistema_marcacao_online.database import get_connection

def obter_cliente_por_telefone(telefone: str):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT id_cliente, nome, telefone, email
            FROM cliente
            WHERE telefone = %s
            """,
            (telefone,),
        ).fetchone()


def registar_cliente(nome: str, telefone: str, email: str) -> int:
    with get_connection() as connection:
        resultado = connection.execute(
            """
            INSERT INTO cliente (nome, telefone, email)
            VALUES (%s, %s, %s)
            RETURNING id_cliente
            """,
            (nome, telefone, email),
        ).fetchone()

        return resultado[0]