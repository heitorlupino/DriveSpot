from db.conexao import conectar


def testar_conexao():

    conexao = conectar()

    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("SHOW TABLES")

            print("Tabelas encontradas no banco: ")
            for tabela in cursor:
                print(tabela)

        except Exception as e:
            print(f"Erro ao listar tabelas: {e}")

        finally:
            cursor.close()
            conexao.close()
            print("Conexão encerrada com sucesso")
    else:
        print("Não foi possível conectar ao banco de dados")

if __name__ == "__main__":
    testar_conexao()