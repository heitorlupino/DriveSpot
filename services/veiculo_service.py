from db.conexao import criar_conexao

def cadastrar_veiculo(id_usuario, id_marca, ano, modelo, preco):
    conn = criar_conexao()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()

        # iniciar transação
        cursor.execute("BEGIN")

        # Inserir veículo
        cursor.execute("""
            INSERT INTO Veiculos (id_usuario, id_marca, ano, modelo, preco)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_usuario, id_marca, ano, modelo, preco))

        # aqui você poderia adicionar lógica adicional
        # ex: inserir categoria na tabela intermediária

        conn.commit()
        print("Veículo cadastrado com sucesso!")
        return True
    except Exception as e:
        conn.rollback()
        print(f"Erro ao cadastrar veículo: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
