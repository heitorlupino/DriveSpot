from db.conexao import conectar as criar_conexao

def criar_categoria(nome):
    conn = criar_conexao()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Categorias (nome)
            VALUES (%s)
        """, (nome,))
        conn.commit()
        print("Categoria criada com sucesso!")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao inserir categoria: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def listar_categorias():
    conn = criar_conexao()
    if conn is None:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Categorias")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar categorias: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
