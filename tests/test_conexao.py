from db.conexao import conectar

conexao = conectar()

if conexao:
    cursor = conexao.cursor()
    cursor.execute("SHOW TABLES")

    print("Tabelas encontradas no banco: ")
    for tabela in cursor:
        print(tabela)

    cursor.close()
    conexao.close()