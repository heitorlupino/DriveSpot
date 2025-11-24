from db.conexao import conectar as criar_conexao

def criar_veiculo(modelo, ano, preco, id_marca, id_usuario):
    conn = criar_conexao()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Veiculos (modelo, ano, preco, id_marca, id_usuario)
            VALUES (%s, %s, %s, %s, %s)
        """, (modelo, ano, preco, id_marca, id_usuario))
        conn.commit()
        print("Veículo criado com sucesso!")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao inserir veículo: {e}")
    finally:
        cursor.close()
        conn.close()

def listar_veiculos():
    conn = criar_conexao()
    if conn is None:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT V.id_veiculo, V.modelo, V.ano, V.preco, M.nome AS marca
            FROM Veiculos V
            JOIN Marcas M ON V.id_marca = M.id_marca
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar veículos: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
