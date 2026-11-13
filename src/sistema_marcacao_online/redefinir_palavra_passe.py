from getpass import getpass

from werkzeug.security import generate_password_hash

from sistema_marcacao_online.database import get_connection


def main():
    email = input("Email do administrador: ").strip().lower()
    nova_palavra_passe = getpass("Nova palavra-passe (mínimo 8 caracteres): ")
    confirmacao = getpass("Confirme a palavra-passe: ")

    if len(nova_palavra_passe) < 8:
        print("A palavra-passe deve ter pelo menos 8 caracteres.")
        return

    if nova_palavra_passe != confirmacao:
        print("As palavras-passe não coincidem.")
        return

    palavra_passe_hash = generate_password_hash(nova_palavra_passe)

    with get_connection() as connection:
        resultado = connection.execute(
            """
            UPDATE administrador
            SET palavra_passe = %s
            WHERE email = %s
            RETURNING id_admin
            """,
            (palavra_passe_hash, email),
        ).fetchone()

    if resultado:
        print("Palavra-passe atualizada. Tenta iniciar sessão novamente.")
    else:
        print("Não existe administrador com esse email.")


if __name__ == "__main__":
    main()