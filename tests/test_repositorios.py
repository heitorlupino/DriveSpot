import pytest
from db.repositorio_usuarios import criar_usuario, listar_usuarios
from db.repositorio_veiculos import criar_veiculo, listar_veiculos
from db.repositorio_marcas import criar_marca, listar_marcas
from db.repositorio_categorias import criar_categoria, listar_categorias
from db.repositorio_veiculosCategorias import vincular_veiculo_categoria, listar_vinculos

def test_criar_e_listar_usuario():
    criar_usuario("Teste", "teste@example.com", "123abc")
    criar_usuario("Teste2", "teste2@email.com", "456dfg")
    usuarios = listar_usuarios()
    emails = [u["email"] for u in usuarios]
    assert "teste@example.com" in emails
    assert "teste2@email.com" in emails

def test_criar_e_listar_marca():
    # Criar uma marca de teste
    criar_marca("Volkswagen")
    criar_marca("Fusca")
    
    # Listar marcas
    marcas = listar_marcas()
    nomes = [m["nome"] for m in marcas]
    
    assert "Volkswagen" in nomes
    assert "Fusca" in nomes

    print("✅ Marca criada e listada com sucesso!")

def test_criar_e_listar_veiculo():
    # Criar um veículo de teste (passando usuario_id)
    criar_veiculo("Volkswagen", 1980, 15000, 1, 1)
    criar_veiculo("Fusca", 1995, 8400, 2, 49)
    
    # Listar veículos
    veiculos = listar_veiculos()
    modelos = [v["modelo"] for v in veiculos]
    
    assert "Volkswagen" in modelos
    assert "Fusca" in modelos
    print("✅ Veículo criado e listado com sucesso!")

def test_criar_e_listar_categoria():
    # Criar categorias de teste
    criar_categoria("SUV")
    criar_categoria("Sedan")
    
    # Listar categorias
    categorias = listar_categorias()
    nomes = [c["nome"] for c in categorias]
    
    assert "SUV" in nomes
    assert "Sedan" in nomes
    print("✅ Categoria criada e listada com sucesso!")


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