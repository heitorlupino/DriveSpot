from db.conexao import conectar

def cadastrar_veiculo(id_usuario, id_marca, ano, modelo, preco):
    conn = conectar()
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

def buscar_veiculos_por_texto(texto):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    like = f"%{texto}%"
    query = """
        SELECT v.id_veiculo, v.modelo, v.ano, v.preco, m.nome AS marca
        FROM veiculos v
        JOIN marcas m ON v.id_marca = m.id_marca
        WHERE CONCAT(m.nome, ' ', v.modelo, ' ', v.ano) LIKE %s
        ORDER BY v.id_veiculo DESC
    """

    cursor.execute(query, (like,))
    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()
    return resultado


def remover_veiculo(id_veiculo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM veiculos WHERE id_veiculo = %s", (id_veiculo,))
    conexao.commit()

    cursor.close()
    conexao.close()


def buscar_por_id(id_veiculo):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT v.id_veiculo, v.modelo, v.ano, v.preco, m.nome AS marca
        FROM veiculos v
        JOIN marcas m ON v.id_marca = m.id_marca
        WHERE id_veiculo = %s
    """, (id_veiculo,))

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()
    return resultado

def atualizar_veiculo(id_veiculo, id_marca, ano, modelo, preco):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE veiculos
        SET id_marca = %s, ano = %s, modelo = %s, preco = %s
        WHERE id_veiculo = %s
    """, (id_marca, ano, modelo, preco, id_veiculo))

    conexao.commit()

    cursor.close()
    conexao.close()