import pytest
from veiculo_service import cadastrar_veiculo
from db.conexao import criar_conexao



def test_cadastrar_veiculo_sucesso():
    resultado = cadastrar_veiculo(1, 1, 2020, "TesteModelo", 50000)
    assert resultado is True

    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Veiculos WHERE modelo=%s AND ano=%s", ("TesteModelo", 2020))
    veiculo = cursor.fetchone()
    cursor.close()
    conn.close()

    assert veiculo is not None

def test_cadastrar_veiculo_erro():
    resultado = cadastrar_veiculo(1, 99999, 2020, "ModeloErro", 50000)
    assert resultado is False
