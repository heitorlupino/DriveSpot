import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexao = mysql.connector.connect(
            host = '127.0.0.1',
            user = 'root',
            password = 'meubanco1004',
            database = 'galeria_veiculos'
        )

        if conexao.is_connected():
            print("Conexão bem sucedidad ao MySQL")
            return conexao
        
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None