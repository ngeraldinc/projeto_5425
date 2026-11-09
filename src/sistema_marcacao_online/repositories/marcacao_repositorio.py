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

def listar_marcacoes():
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT
                m.id_marcacao,
                m.data,
                m.hora,
                m.estado,
                c.nome,
                COALESCE(STRING_AGG(s.nome, ', '), 'Sem serviços')
            FROM marcacao AS m
            JOIN cliente AS c
                ON c.id_cliente = m.id_cliente
            LEFT JOIN marcacao_servico AS ms
                ON ms.id_marcacao = m.id_marcacao
            LEFT JOIN servico AS s
                ON s.id_servico = ms.id_servico
            GROUP BY
                m.id_marcacao,
                m.data,
                m.hora,
                m.estado,
                c.nome
            ORDER BY m.data, m.hora
            """
        ).fetchall()

def atualizar_estado_marcacao(id_marcacao: int, estado: str):
    with get_connection() as connection:
        resultado = connection.execute(
            """
            UPDATE marcacao
            SET estado = %s
            WHERE id_marcacao = %s
            RETURNING id_marcacao
            """,
            (estado, id_marcacao),
        ).fetchone()

    return resultado[0] if resultado else None

def listar_horarios_ocupados(data: date) -> list[time]:
    with get_connection() as connection:
        resultados = connection.execute(
            """
            SELECT hora
            FROM marcacao
            WHERE data = %s
              AND estado <> 'cancelada'
            """,
            (data,),
        ).fetchall()

    return [resultado[0] for resultado in resultados]