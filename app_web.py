from flask import Flask, render_template, request, redirect, url_for, flash
from services.veiculo_service import cadastrar_veiculo, buscar_veiculos_por_texto, remover_veiculo, buscar_por_id, atualizar_veiculo

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

@app.route('/remover', methods=['GET', 'POST'])
def remover():
    pesquisa = request.form.get("pesquisa", "")
    resultados = []

    if request.method == "POST" and request.form.get("acao") == "pesquisar":
        resultados = buscar_veiculos_por_texto(pesquisa)

    return render_template("remover.html",
                           resultados=resultados,
                           pesquisa=pesquisa)


@app.route('/confirmar-remocao/<int:id_veiculo>')
def confirmar_remocao(id_veiculo):
    veiculo = buscar_por_id(id_veiculo)
    if not veiculo:
        flash("Veículo não encontrado.")
        return redirect(url_for("remover"))
    return render_template("confirmar_remocao.html", veiculo=veiculo)


@app.route('/remover/<int:id_veiculo>', methods=['POST'])
def remover_final(id_veiculo):
    remover_veiculo(id_veiculo)
    flash("✅ Veículo removido com sucesso!")
    return redirect(url_for("remover"))

@app.route('/editar/<int:id_veiculo>', methods=['GET', 'POST'])
def editar_veiculo(id_veiculo):
    veiculo = buscar_por_id(id_veiculo)

    if not veiculo:
        flash("❌ Veículo não encontrado!")
        return redirect('/')

    if request.method == 'POST':
        modelo = request.form['modelo']
        marca = request.form['marca']
        ano = int(request.form['ano'])
        preco = float(request.form['preco'])

        id_marca = buscar_id_marca(marca) 

        try:
            atualizar_veiculo(id_veiculo, id_marca, ano, modelo, preco)
            flash("✅ Veículo atualizado com sucesso!")
            return redirect('/')  
        except Exception as e:
            flash(f"❌ Erro ao atualizar veículo: {e}")


    return render_template('editar.html', veiculo=veiculo)

@app.route('/editar')
def escolher_veiculo_editar():
    # essa tela abre vazia, igual você quer
    return render_template('editar.html', veiculo=None)


        

if __name__ == "__main__":
    app.run(debug=True)
