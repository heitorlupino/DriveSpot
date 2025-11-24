from db.conexao import conectar as criar_conexao

def vincular_veiculo_categoria(id_veiculo, id_categoria):
    conn = criar_conexao()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Veiculos_Categorias (id_veiculo, id_categoria)
            VALUES (%s, %s)
        """, (id_veiculo, id_categoria))
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
                VC.id_veiculo,
                V.modelo AS veiculo,
                C.nome AS categoria
            FROM Veiculos_Categorias VC
            JOIN Veiculos V ON VC.id_veiculo = V.id_veiculo
            JOIN Categorias C ON VC.id_categoria = C.id_categoria
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar vínculos: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
