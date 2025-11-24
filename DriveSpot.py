from services.veiculo_service import cadastrar_veiculo

def menu():
    print("===== DRIVE SPOT =====")
    print("1 - Cadastrar veículo")
    print("0 - Sair")
    return input("Escolha uma opção: ")

def main():
    while True:
        opcao = menu()
        if opcao == "1":
            id_usuario = int(input("ID do usuário: "))
            id_marca = int(input("ID da marca: "))
            ano = int(input("Ano do veículo: "))
            modelo = input("Modelo do veículo: ")
            preco = float(input("Preço do veículo: "))

            cadastrar_veiculo(id_usuario, id_marca, ano, modelo, preco)
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
