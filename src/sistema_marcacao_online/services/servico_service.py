from decimal import Decimal , InvalidOperation
from sistema_marcacao_online.database import get_connection
from sistema_marcacao_online.repositories.servico_repository import (
    listar_servicos as listar_servicos_repo,
    registar_servico as guardar_servico,
)


def listar_servicos():
    return listar_servicos_repo()

CENTIMO = Decimal("0.01")
PRECO_MAXIMO = Decimal("99999999.99")


def _validar_texto(valor: str, campo: str, limite: int) -> str:
    if not isinstance(valor, str):
        raise ValueError(f"O {campo} deve ser texto.")

    texto = valor.strip()

    if not texto:
        raise ValueError(f"O {campo} é obrigatório e não pode ficar vazio.")

    if len(texto) > limite:
        raise ValueError(
            f"O {campo} deve ter no máximo {limite} caracteres "
            f"(atualmente tem {len(texto)})."
        )

    return texto


def criar_servico(nome: str, descricao: str, preco: str | Decimal) -> int:
    nome_validado = _validar_texto(nome, "nome", 50)
    descricao_validada = _validar_texto(descricao, "descrição", 100)

    try:
        texto_preco = str(preco).strip().replace(",", ".")
        preco_validado = Decimal(texto_preco)
    except (InvalidOperation, ValueError):
        raise ValueError("O preço deve ser um valor monetário válido, por exemplo 12.50.")

    if not preco_validado.is_finite():
        raise ValueError("O preço deve ser um número finito.")

    if preco_validado < 0:
        raise ValueError("O preço não pode ser negativo.")

    if preco_validado > PRECO_MAXIMO:
        raise ValueError("O preço não pode exceder 99 999 999.99.")

    if preco_validado != preco_validado.quantize(CENTIMO):
        raise ValueError("O preço pode ter no máximo duas casas decimais.")

    return guardar_servico(nome_validado, descricao_validada, preco_validado)