import mysql.connector
import os
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def conectar():
    try:
        conexao = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if conexao.is_connected():
            print("Conexão bem sucedidad ao MySQL")
            return conexao
        
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None