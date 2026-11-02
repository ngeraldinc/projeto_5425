from sistema_marcacao_online.services.servico_service import (
    criar_servico,
    listar_servicos,
)
from sistema_marcacao_online.services.cliente_servico import (
    obter_ou_registar_cliente,
)
def mostrar_servicos():
    try:
        servicos = listar_servicos()

        if not servicos:
            print("\nAinda não existem serviços registados.")
            return

        print("\nServiços disponíveis:")
        for id_servico, nome, descricao, preco in servicos:
            print(f"{id_servico}. {nome} — {descricao} — {preco} €")

    except Exception as erro:
        print(f"\nNão foi possível listar os serviços: {erro}")


def registar_novo_servico():
    print("\nRegistar serviço")
    nome = input("Nome: ")
    descricao = input("Descrição: ")
    preco = input("Preço: ")

    try:
        id_servico = criar_servico(nome, descricao, preco)
        print(f"Serviço registado com sucesso. ID: {id_servico}")

    except ValueError as erro:
        print(f"Dados inválidos: {erro}")

    except Exception as erro:
        print(f"Não foi possível registar o serviço: {erro}")

def registar_novo_cliente():
    print("\nRegistar cliente")
    nome = input("Nome: ")
    telefone = input("Telefone: ")
    email = input("Email: ")

    try:
        id_cliente = obter_ou_registar_cliente(nome, telefone, email)
        print(f"Cliente registado ou encontrado. ID: {id_cliente}")

    except ValueError as erro:
        print(f"Dados inválidos: {erro}")

    except Exception as erro:
        print(f"Não foi possível registar o cliente: {erro}")

def main():
    while True:
        print("\n=== Sistema de marcações ===")
        print("1. Listar serviços")
        print("2. Registar serviço")
        print("3. Registar cliente")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            mostrar_servicos()
        elif opcao == "2":
            registar_novo_servico()
        elif opcao == "3":
            registar_novo_cliente()
        elif opcao == "0":
            print("A aplicação foi encerrada.")
            break
        else:
            print("Opção inválida. Escolha 1, 2 , 3 ou 0.")

if __name__ == "__main__":
    main()