from flask import Flask, render_template, request, redirect, url_for, flash
from services.veiculo_service import cadastrar_veiculo

app = Flask(__name__)
app.secret_key = "algumasecretkey"

@app.route('/')
def index():
    # Redireciona para a página de adicionar veículo
    return render_template('adicionar.html')


@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_veiculo():
    if request.method == 'POST':
        modelo = request.form['modelo']
        marca = request.form['marca']
        ano = int(request.form['ano'])
        preco = float(request.form['preco'])

        # IDs automáticos (exemplo)
        id_usuario = 1  # o usuário logado, futuramente isso virá da sessão
        id_marca = buscar_id_marca(marca)  # função que encontra ou cria a marca

        try:
            cadastrar_veiculo(id_usuario, id_marca, ano, modelo, preco)
            flash("✅ Veículo cadastrado com sucesso!")
        except Exception as e:
            flash(f"❌ Erro ao cadastrar veículo: {e}")
        
    return render_template('adicionar.html')


def buscar_id_marca(nome_marca):
    import mysql.connector
    from db.conexao import conectar as obter_conexao

    conexao = obter_conexao()
    cursor = conexao.cursor()

    # Verifica se a marca já existe
    cursor.execute("SELECT id_marca FROM marcas WHERE nome = %s", (nome_marca,))
    resultado = cursor.fetchone()

    if resultado:
        id_marca = resultado[0]
    else:
        # Cria a marca se não existir
        cursor.execute("INSERT INTO marcas (nome) VALUES (%s)", (nome_marca,))
        conexao.commit()
        id_marca = cursor.lastrowid

    cursor.close()
    conexao.close()
    return id_marca

if __name__ == "__main__":
    app.run(debug=True)
