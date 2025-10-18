from db.repositorio_usuarios import criar_usuario, listar_usuarios

# Teste de inserção
criar_usuario("João Pedro", "joao@example.com", "hash_senha_teste")

# Teste de listagem
usuarios = listar_usuarios()
for u in usuarios:
    print(u)
