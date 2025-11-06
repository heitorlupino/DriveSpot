from flask import Flask, render_template, request, redirect, url_for, flash
from services.veiculo_service import cadastrar_veiculo, buscar_veiculos_por_texto, remover_veiculo, buscar_por_id, buscar_veiculo_exato, atualizar_veiculo

app = Flask(__name__)
app.secret_key = "algumasecretkey"

@app.route('/')
def index():
    
    return render_template('adicionar.html')


@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_veiculo():
    if request.method == 'POST':
        modelo = request.form['modelo']
        marca = request.form['marca']
        ano = int(request.form['ano'])
        preco = float(request.form['preco'])

        
        id_usuario = 1  
        id_marca = buscar_id_marca(marca)  

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

  
    cursor.execute("SELECT id_marca FROM marcas WHERE nome = %s", (nome_marca,))
    resultado = cursor.fetchone()

    if resultado:
        id_marca = resultado[0]
    else:
        
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

@app.route("/editar", methods=["GET", "POST"])
def editar():
    veiculo = None
    mensagem = ""

    if request.method == "POST":

        # --- PESQUISAR ---
        if "pesquisar" in request.form:
            termo = request.form.get("pesquisa")
            veiculo = buscar_veiculo_exato(termo)

            if not veiculo:
                mensagem = "❌ Nenhum veículo encontrado com esse modelo."

        # --- SALVAR ALTERAÇÕES ---
        elif "salvar" in request.form:
            id_veiculo = request.form.get("id_veiculo")
            modelo = request.form.get("modelo")
            marca = request.form.get("marca")
            ano = request.form.get("ano")
            preco = request.form.get("preco")

            atualizar_veiculo(id_veiculo, modelo, marca, ano, preco)
            mensagem = "✅ Veículo atualizado com sucesso!"

            # Recarrega os dados atualizados
            veiculo = buscar_por_id(id_veiculo)

    return render_template("editar.html", veiculo=veiculo, mensagem=mensagem)



if __name__ == "__main__":
    app.run(debug=True)
