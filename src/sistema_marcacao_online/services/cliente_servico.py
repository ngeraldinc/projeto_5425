from sistema_marcacao_online.repositories.cliente_repositorio import (
    obter_cliente_por_telefone,
    registar_cliente,
)

def _validar_texto(valor: str, campo: str, limite: int) -> str:
    if not isinstance(valor, str):
        raise ValueError(f"{campo} deve ser texto.")

    texto = valor.strip()

    if not texto:
        raise ValueError(f"{campo} é obrigatório.")

    if len(texto) > limite:
        raise ValueError(f"{campo} deve ter no máximo {limite} caracteres.")

    return texto


def obter_ou_registar_cliente(nome: str, telefone: str, email: str) -> int:
    nome_validado = _validar_texto(nome, "O nome", 100)
    telefone_validado = _validar_texto(telefone, "O telefone", 30)
    email_validado = _validar_texto(email, "O email", 50)

    if "@" not in email_validado:
        raise ValueError("Introduza um email válido, por exemplo nome@email.com.")

    cliente = obter_cliente_por_telefone(telefone_validado)

    if cliente:
        return cliente[0]

    return registar_cliente(nome_validado, telefone_validado, email_validado)