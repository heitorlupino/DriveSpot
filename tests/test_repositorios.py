import pytest
from db.repositorio_usuarios import criar_usuario, listar_usuarios
from db.repositorio_veiculos import criar_veiculo, listar_veiculos
from db.repositorio_marcas import criar_marca, listar_marcas
from db.repositorio_categorias import criar_categoria, listar_categorias
from db.repositorio_veiculosCategorias import vincular_veiculo_categoria, listar_vinculos

def test_criar_e_listar_usuario():
    criar_usuario("Teste3", "meuteste@gmail.com", "ggg123")
    usuarios = listar_usuarios()
    emails = [u["email"] for u in usuarios]
    assert "meuteste@gmail.com" in emails

def test_criar_e_listar_marca():
    # criar_marca("Volkswagen")
    # criar_marca("Fusca")
    #criar_marca("Chevrolet")
    criar_marca("Toyota")
    marcas = listar_marcas()
    nomes = [m["nome"] for m in marcas]
    
    # assert "Volkswagen" in nomes
    # assert "Fusca" in nomes
    # assert "Chevrolet" in nomes
    assert "Toyota" in nomes

    print("Marca criada e listada com sucesso!")

def test_criar_e_listar_veiculo():
    # criar_veiculo("Volkswagen", 1980, 15000, 1, 1)
    # criar_veiculo("Fusca", 1995, 8400, 2, 49)
    criar_veiculo("Onix", 2012, 120000, 3, 87)
    
    
    veiculos = listar_veiculos()
    modelos = [v["modelo"] for v in veiculos]
    
    # assert "Volkswagen" in modelos
    # assert "Fusca" in modelos
    assert "Onix" in modelos
    print("Veículo criado e listado com sucesso!")

def test_criar_e_listar_categoria():
    # criar_categoria("SUV")
    # criar_categoria("Sedan")
    criar_categoria("Hatch compacto")
    
    # Listar categorias
    categorias = listar_categorias()
    nomes = [c["nome"] for c in categorias]
    
    # assert "SUV" in nomes
    # assert "Sedan" in nomes
    assert "Hatch compacto" in nomes
    print("Categoria criada e listada com sucesso!")

def test_vincular_e_listar_veiculosCategorias():
    # IDs que você já criou manualmente no banco
    id_veiculo = 30       # substitua pelo ID do veículo que você criou
    id_categoria = 14     # substitua pelo ID da categoria que você criou

    # Vincular veículo à categoria
    vincular_veiculo_categoria(id_veiculo, id_categoria)

    # Listar vínculos
    vinculos = listar_vinculos()

    # Verificar se o vínculo criado existe
    encontrado = any(v['id_veiculo'] == id_veiculo and v['categoria'] == "Hatch compacto" for v in vinculos)
    assert encontrado, "Vínculo veículo-categoria não encontrado"

def test_criar_usuario_email_duplicado_try_except():
    try:
        criar_usuario("Usuário1", "teste_duplicado@example.com", "senha123")

        criar_usuario("Usuário2", "teste_duplicado@example.com", "senha456")

        print("ERRO: O sistema permitiu criar um usuário com email duplicado!")
    except Exception as e:
        print("SUCESSO: o sistema impediu email duplicado.")
        print(f"Detalhes do erro: {e}")

    usuarios = listar_usuarios()
    emails = [u["email"] for u in usuarios]
    assert emails.count("teste_duplicado@example.com") == 1

def test_criar_marca_invalida():
    try:
        criar_marca(None) 
        print("ERRO: O sistema aceitou uma marca sem nome!")
        assert False, "Marca inválida foi inserida sem erro!"
    except Exception as e:
        print("SUCESSO: o sistema impediu criar uma marca inválida.")
        print(f"Detalhes do erro: {e}")

    marcas = listar_marcas()
    nomes = [m["nome"] for m in marcas]
    assert None not in nomes, "Foi encontrada uma marca com nome None!"

def test_criar_veiculo_invalido():

    criar_veiculo(None, 2020, 50000.0, 9999, 1) 

    veiculos = listar_veiculos()
    modelos = [v["modelo"] for v in veiculos]

    if None in modelos:
        print("ERRO: O sistema permitiu criar um veículo com modelo nulo!")
        assert False, "Veículo inválido foi inserido no banco!"
    else:
        print("SUCESSO: o sistema impediu criar veículo com dados inválidos.")

def test_criar_categoria_invalida():
    try:
        criar_categoria(None)
        print("ERRO: o sistema aceitou uma categoria sem nome!")
        assert False, "Categoria inválida foi inserida sem erro!"
    except Exception as e:
        print("SUCESSO: o sistema impediu criar uma categoria com nome NONE!")
        print(f"Detalher do erro: {e}")
    
    categorias = listar_categorias()
    nomes = [m["nome"] for m in categorias]
    assert None not in nomes, "Foi encontrado uma categoria com nome NONE!"

def test_criar_veiculosCategoria_invalidos():
    
    vincular_veiculo_categoria(909090, 828282)

    vinculos = listar_vinculos()

    for v in vinculos:
        if v["id_veiculo"] == 909090 or v["categoria"] == 828282:
            print("ERRO: O sistema permitiu criar um vínculo inválido!")
            assert False, "Vínculo inválido foi inserido!"
    
    print("SUCESSO: o sistema impediu criar vínculo com dados inválidos.")