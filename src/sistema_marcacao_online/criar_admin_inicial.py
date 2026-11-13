from getpass import getpass

from sistema_marcacao_online.services.administrador_servico import (
    criar_administrador,
)


def main():
    print("Criar administrador inicial")
    nome = input("Nome: ").strip()
    email = input("Email: ").strip()
    palavra_passe = getpass("Palavra-passe: ")
    confirmacao = getpass("Confirme a palavra-passe: ")

    if palavra_passe != confirmacao:
        print("As palavras-passe não coincidem.")
        return

    try:
        id_admin = criar_administrador(nome, email, palavra_passe)
        print(f"Administrador criado com sucesso. ID: {id_admin}")
    except ValueError as erro:
        print(f"Dados inválidos: {erro}")
    except Exception as erro:
        print(f"Não foi possível criar o administrador: {erro}")


if __name__ == "__main__":
    main()