import os
from db.conexao import conectar
from werkzeug.security import generate_password_hash
from collections import Counter
from flask import current_app

def cadastrar_usuario(nome, email, senha):
    conexao = conectar()
    if conexao is None:
        return False

    try:
        cursor = conexao.cursor()

        # Criptografar a senha antes de salvar
        senha_hash = generate_password_hash(senha)

        cursor.execute("""
            INSERT INTO Usuarios (nome, email, senha_hash)
            VALUES (%s, %s, %s)
        """, (nome, email, senha_hash))
        
        conexao.commit()
        print("Usuário cadastrado com sucesso!")
        return True

    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")
        conexao.rollback()
        return False

    finally:
        cursor.close()
        conexao.close()

def cadastrar_veiculo(id_usuario, id_marca, ano, modelo, preco, imagem_url=None):
    conn = conectar()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()

        # iniciar transação
        cursor.execute("BEGIN")

        # Inserir veículo
        cursor.execute("""
            INSERT INTO Veiculos (id_usuario, id_marca, ano, modelo, preco, imagem_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_usuario, id_marca, ano, modelo, preco, imagem_url))

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
    cursor = conexao.cursor(dictionary=True)

    try:
        # Buscar a imagem associada ao veículo
        cursor.execute("SELECT imagem_url FROM Veiculos WHERE id_veiculo = %s", (id_veiculo,))
        row = cursor.fetchone()

        # Deletar imagem antiga, se existir
        if row and row.get("imagem_url"):
            caminho_relativo = row["imagem_url"].lstrip("/")  # remove a barra inicial
            caminho_absoluto = os.path.join(current_app.root_path, caminho_relativo)

            if os.path.exists(caminho_absoluto):
                try:
                    os.remove(caminho_absoluto)
                except Exception:
                    pass  # evita quebrar o fluxo caso dê erro

        # Remover o veículo do banco de dados
        cursor.execute("DELETE FROM Veiculos WHERE id_veiculo = %s", (id_veiculo,))
        conexao.commit()

    finally:
        cursor.close()
        conexao.close()


def buscar_por_id(id_veiculo):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT v.id_veiculo, v.modelo, v.ano, v.preco, v.imagem_url, m.nome AS marca
        FROM veiculos v
        JOIN marcas m ON v.id_marca = m.id_marca
        WHERE id_veiculo = %s
    """, (id_veiculo,))

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()
    return resultado

def buscar_veiculo_exato(nome):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True, buffered=True)

    try:
        partes = nome.split()

        sql = """
            SELECT v.id_veiculo, v.modelo, m.nome AS marca, v.ano, v.preco
            FROM veiculos v
            INNER JOIN marcas m ON v.id_marca = m.id_marca
            WHERE CONCAT(m.nome, ' ', v.modelo, ' ', v.ano) LIKE %s
        """

        nome_busca = f"%{' '.join(partes)}%"
        cursor.execute(sql, (nome_busca,))
        veiculo = cursor.fetchone()

        return veiculo

    finally:
        cursor.close()
        conexao.close()

def atualizar_veiculo(id_veiculo, modelo, nome_marca, ano, preco, imagem_url):
    conexao = conectar()
    cursor = conexao.cursor()

    # Buscar o id_marca correspondente ao nome da marca
    cursor.execute("SELECT id_marca FROM marcas WHERE nome = %s", (nome_marca,))
    resultado = cursor.fetchone()

    if not resultado:
        raise ValueError(f"Marca '{nome_marca}' não encontrada no banco de dados.")

    id_marca = resultado[0]

    # Atualizar o veículo com o id_marca correto
    query = """
        UPDATE veiculos
        SET modelo = %s, id_marca = %s, ano = %s, preco = %s, imagem_url = %s
        WHERE id_veiculo = %s
    """
    cursor.execute(query, (modelo, id_marca, ano, preco, id_veiculo, imagem_url))
    conexao.commit()

    cursor.close()
    conexao.close()

def gerar_relatorio(filtros):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    query = """
        SELECT v.modelo, m.nome AS marca, v.ano, v.preco
        FROM Veiculos v
        INNER JOIN Marcas m ON v.id_marca = m.id_marca
        WHERE 1=1
    """
    valores = []

    if filtros["marca"]:
        query += " AND m.nome = %s"
        valores.append(filtros["marca"])

    if filtros["ano_min"]:
        query += " AND v.ano >= %s"
        valores.append(filtros["ano_min"])

    if filtros["ano_max"]:
        query += " AND v.ano <= %s"
        valores.append(filtros["ano_max"])

    if filtros["preco_max"]:
        query += " AND v.preco <= %s"
        valores.append(filtros["preco_max"])

    cursor.execute(query, valores)
    veiculos = cursor.fetchall()

    if not veiculos:
        return None

    # Estatísticas
    total = len(veiculos)
    media_preco = sum(v["preco"] for v in veiculos) / total
    marca_comum = Counter(v["marca"] for v in veiculos).most_common(1)[0][0]
    ano_frequente = Counter(v["ano"] for v in veiculos).most_common(1)[0][0]

    cursor.close()
    conexao.close()

    return {
        "total": total,
        "media_preco": round(media_preco, 2),
        "marca_comum": marca_comum,
        "ano_frequente": ano_frequente,
        "veiculos": veiculos
    }

