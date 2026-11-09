from sistema_marcacao_online.services.servico_servico import criar_servico, listar_servicos
from sistema_marcacao_online.services.cliente_servico import obter_ou_registar_cliente
from sistema_marcacao_online.services.marcacao_servico import criar_marcacao, atualizar_estado_marcacao, listar_marcacoes, listar_horarios_disponiveis, listar_marcacoes

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

def registar_nova_marcacao():
    print("\nRegistar marcação")
    data = input("Data (AAAA-MM-DD): ").strip()

    try:
        horarios = listar_horarios_disponiveis(data)
    except ValueError as erro:
        print(f"Data inválida: {erro}")
        return
    except Exception as erro:
        print(f"Não foi possível consultar os horários: {erro}")
        return

    if not horarios:
        print("Não existem horários disponíveis nessa data.")
        return

    print(f"\nHorários disponíveis para {data}:")
    for hora_disponivel in horarios:
        print(hora_disponivel.strftime("%H:%M"))

    hora = input("Escolha uma hora disponível (HH:MM): ").strip()
    id_cliente = input("ID do cliente: ").strip()
    ids_servicos = input("IDs dos serviços separados por vírgulas: ").strip()

    try:
        id_marcacao = criar_marcacao(
            int(id_cliente),
            data,
            hora,
            ids_servicos,
        )
        print(f"Marcação criada com sucesso. ID: {id_marcacao}")

    except ValueError as erro:
        print(f"Dados inválidos: {erro}")

    except Exception as erro:
        print(f"Não foi possível criar a marcação: {erro}")

def mostrar_marcacoes():
    try:
        marcacoes = listar_marcacoes()

        if not marcacoes:
            print("\nAinda não existem marcações registadas.")
            return

        print("\nMarcações:")
        for id_marcacao, data, hora, estado, nome_cliente, servicos in marcacoes:
            print(
                f"{id_marcacao}. {data} às {hora} — {nome_cliente} — "
                f"{servicos} — Estado: {estado}"
            )

    except Exception as erro:
        print(f"\nNão foi possível listar as marcações: {erro}")

def atualizar_estado_marcacao_menu():
    print("\nAtualizar estado da marcação")
    id_marcacao = input("ID da marcação: ").strip()
    estado = input("Novo estado (realizada, cancelada ou falta): ").strip()

    try:
        id_atualizado = atualizar_estado_marcacao(
            int(id_marcacao),
            estado,
        )
        print(f"Estado da marcação {id_atualizado} atualizado com sucesso.")

    except ValueError as erro:
        print(f"Dados inválidos: {erro}")

    except Exception as erro:
        print(f"Não foi possível atualizar a marcação: {erro}")

def mostrar_horarios_disponiveis():
    data = input("Data (AAAA-MM-DD): ").strip()

    try:
        horarios = listar_horarios_disponiveis(data)

        if not horarios:
            print("\nNão existem horários disponíveis nessa data.")
            return

        print(f"\nHorários disponíveis para {data}:")
        for hora in horarios:
            print(hora.strftime("%H:%M"))

    except ValueError as erro:
        print(f"Data inválida: {erro}")

    except Exception as erro:
        print(f"Não foi possível consultar os horários: {erro}")

def main():
    while True:
        print("\n=== Sistema de marcações ===")
        print("1. Listar serviços")
        print("2. Registar serviço")
        print("3. Registar cliente")
        print("4. Registar marcação")
        print("5. Listar marcações")
        print("6. Atualizar estado de marcação")
        print("7. Consultar horários disponíveis")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            mostrar_servicos()
        elif opcao == "2":
            registar_novo_servico()
        elif opcao == "3":
            registar_novo_cliente()
        elif opcao == "4":
            registar_nova_marcacao()    
        elif opcao == "5":
            mostrar_marcacoes()
        elif opcao == "6":
            atualizar_estado_marcacao_menu()
        elif opcao == "7":
             mostrar_horarios_disponiveis()
        elif opcao == "0":
            print("A aplicação foi encerrada.")
            break
        else:
            print("Opção inválida. Escolha 1, 2 , 3 , 4 , 5 , 6 , 7 ou 0.")

if __name__ == "__main__":
    main()