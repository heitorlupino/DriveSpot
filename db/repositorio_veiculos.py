from db.conexao import conectar as criar_conexao

def criar_veiculo(modelo, ano, preco, marca_id):
    conn = criar_conexao()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Veiculos (modelo, ano, preco, marca_id)
            VALUES (%s, %s, %s, %s)
        """, (modelo, ano, preco, marca_id))
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
            SELECT V.id, V.modelo, V.ano, V.preco, M.nome AS marca
            FROM Veiculos V
            JOIN Marcas M ON V.marca_id = M.id
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar veículos: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
