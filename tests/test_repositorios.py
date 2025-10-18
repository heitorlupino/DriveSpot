import pytest
from db.repositorio_usuarios import criar_usuario, listar_usuarios

def test_criar_e_listar_usuario():
    criar_usuario("Teste", "teste@example.com", "123abc")
    usuarios = listar_usuarios()
    emails = [u["email"] for u in usuarios]
    assert "teste@example.com" in emails

def test_criar_usuario_email_duplicado_try_except():
    try:
        criar_usuario("Usuário1", "teste_duplicado@example.com", "senha123")

        criar_usuario("Usuário2", "teste_duplicado@example.com", "senha456")

        print("❌ ERRO: O sistema permitiu criar um usuário com email duplicado!")
    except Exception as e:
        print("✅ Sucesso: o sistema impediu email duplicado.")
        print(f"Detalhes do erro: {e}")

    usuarios = listar_usuarios()
    emails = [u["email"] for u in usuarios]
    assert emails.count("teste_duplicado@example.com") == 1