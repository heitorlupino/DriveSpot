from db.conexao import conectar as criar_conexao

def criar_marca(nome):
    conn = criar_conexao()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Marcas (nome)
            VALUES (%s)
        """, (nome,))
        conn.commit()
        print("Marca criada com sucesso!")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao inserir marca: {e}")
    finally:
        cursor.close()
        conn.close()

def listar_marcas():
    conn = criar_conexao()
    if conn is None:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Marcas")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar marcas: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
