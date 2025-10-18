from db.conexao import conectar as criar_conexao

def vincular_veiculo_categoria(veiculo_id, categoria_id):
    conn = criar_conexao()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Veiculos_Categorias (veiculo_id, categoria_id)
            VALUES (%s, %s)
        """, (veiculo_id, categoria_id))
        conn.commit()
        print("Veículo vinculado à categoria com sucesso!")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao vincular veículo e categoria: {e}")
    finally:
        cursor.close()
        conn.close()

def listar_vinculos():
    conn = criar_conexao()
    if conn is None:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                VC.id,
                V.modelo AS veiculo,
                C.nome AS categoria
            FROM Veiculos_Categorias VC
            JOIN Veiculos V ON VC.veiculo_id = V.id
            JOIN Categorias C ON VC.categoria_id = C.id
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar vínculos: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
