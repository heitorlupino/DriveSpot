from db.conexao import conectar as criar_conexao

def criar_usuario(nome, email, senha_hash):
    conn = criar_conexao()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Usuarios (nome, email, senha_hash)
            VALUES (%s, %s, %s)
        """, (nome, email, senha_hash))
        conn.commit()
        print("Usuário criado com sucesso!")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao inserir usuário: {e}")
    finally:
        cursor.close()
        conn.close()


def listar_usuarios():
    conn = criar_conexao()
    if conn is None:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Usuarios")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
