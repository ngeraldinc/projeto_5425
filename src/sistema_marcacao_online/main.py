from sistema_marcacao_online.repositories.servico_repository import listar_servicos


def main():
    print("=== Sistema de marcações ===")

    try:
        servicos = listar_servicos()
    except Exception as erro:
        print(f"Erro ao consultar os serviços: {erro}")
        return

    if not servicos:
        print("Ainda não existem serviços registados.")
        return

    print("\nServiços disponíveis:")
    for id_servico, nome, descricao, preco in servicos:
        print(f"{id_servico}. {nome} — {descricao} — {preco} €")


if __name__ == "__main__":
    main()