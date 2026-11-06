from datetime import date, time

from sistema_marcacao_online.database import get_connection


def contar_faltas_cliente(id_cliente: int) -> int:
    with get_connection() as connection:
        resultado = connection.execute(
            """
            SELECT COUNT(*)
            FROM marcacao
            WHERE id_cliente = %s
              AND estado = 'falta'
            """,
            (id_cliente,),
        ).fetchone()

    return resultado[0]


def horario_disponivel(data: date, hora: time) -> bool:
    with get_connection() as connection:
        resultado = connection.execute(
            """
            SELECT NOT EXISTS (
                SELECT 1
                FROM marcacao
                WHERE data = %s
                  AND hora = %s
                  AND estado <> 'cancelada'
            )
            """,
            (data, hora),
        ).fetchone()

    return resultado[0]


def criar_marcacao(
    id_cliente: int,
    data: date,
    hora: time,
    ids_servicos: list[int],
) -> int:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO marcacao (data, hora, estado, id_cliente)
                VALUES (%s, %s, 'confirmada', %s)
                RETURNING id_marcacao
                """,
                (data, hora, id_cliente),
            )
            id_marcacao = cursor.fetchone()[0]

            cursor.executemany(
                """
                INSERT INTO marcacao_servico (id_marcacao, id_servico)
                VALUES (%s, %s)
                """,
                [
                    (id_marcacao, id_servico)
                    for id_servico in ids_servicos
                ],
            )

        return id_marcacao