from flask import Flask, render_template, request, redirect, url_for, flash, session
from db.conexao import conectar as obter_conexao
from services.veiculo_service import cadastrar_veiculo, buscar_veiculos_por_texto, remover_veiculo, buscar_por_id, buscar_veiculo_exato, atualizar_veiculo, cadastrar_usuario


app = Flask(__name__)
app.secret_key = "algumasecretkey"

@app.route('/')
def index():
    
    return render_template('adicionar.html')

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        confirmar_email = request.form.get("confirmar_email")
        senha = request.form.get("senha")
        confirmar_senha = request.form.get("confirmar_senha")

        if email != confirmar_email:
            flash("Os e-mails não coincidem.")
            return render_template("cadastro.html")

        if senha != confirmar_senha:
            flash("As senhas não coincidem.")
            return render_template("cadastro.html")

        try:
            conexao = obter_conexao()
            cursor = conexao.cursor()

            cursor.execute("SELECT id_usuario FROM Usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("Este e-mail já está cadastrado.")
                return render_template("cadastro.html")

            cursor.execute(
                "INSERT INTO Usuarios (nome, email, senha_hash) VALUES (%s, %s, %s)",
                (nome, email, senha) 
            )
            conexao.commit()

            flash("Cadastro realizado com sucesso! Agora você pode fazer login.")
            return redirect(url_for("login"))

        except Exception as e:
            flash(f"Erro ao cadastrar: {e}")

        finally:
            cursor.close()
            conexao.close()

    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        try:
            conexao = obter_conexao()
            cursor = conexao.cursor(dictionary=True)

            # Verifica se o email existe
            cursor.execute("SELECT * FROM Usuarios WHERE email = %s", (email,))
            usuario = cursor.fetchone()

            if usuario and usuario["senha_hash"] == senha:
                session["usuario_nome"] = usuario["nome"]
                return redirect(url_for("index"))
            else:
                flash("E-mail ou senha incorretos.")
                return render_template("login.html")

        except Exception as e:
            flash(f"Erro ao fazer login: {e}")
            return render_template("login.html")

        finally:
            cursor.close()
            conexao.close()

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario_nome", None)
    return redirect(url_for("login"))



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
            flash("Veículo cadastrado com sucesso!")
        except Exception as e:
            flash(f"Erro ao cadastrar veículo: {e}")
        
    return render_template('adicionar.html')


def buscar_id_marca(nome_marca):
    import mysql.connector

    conexao = obter_conexao()
    cursor = conexao.cursor(buffered=True)  # <-- evita o erro de unread result

    try:
        # Verifica se a marca já existe
        cursor.execute("SELECT id_marca FROM marcas WHERE nome = %s", (nome_marca,))
        resultado = cursor.fetchone()

        if resultado:
            id_marca = resultado[0]
        else:
            # Insere nova marca se não existir
            cursor.execute("INSERT INTO marcas (nome) VALUES (%s)", (nome_marca,))
            conexao.commit()
            id_marca = cursor.lastrowid

        return id_marca

    except mysql.connector.Error as erro:
        print(f"Erro ao buscar ou inserir marca: {erro}")
        conexao.rollback()
        return None

    finally:
        cursor.close()
        conexao.close()


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
    flash("Veículo removido com sucesso!")
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
                mensagem = "Nenhum veículo encontrado com esse modelo."

        # --- SALVAR ALTERAÇÕES ---
        elif "salvar" in request.form:
            id_veiculo = request.form.get("id_veiculo")
            modelo = request.form.get("modelo")
            marca = request.form.get("marca")
            ano = request.form.get("ano")
            preco = request.form.get("preco")

            atualizar_veiculo(id_veiculo, modelo, marca, ano, preco)
            mensagem = "Veículo atualizado com sucesso!"

            # Recarrega os dados atualizados
            veiculo = buscar_por_id(id_veiculo)

    return render_template("editar.html", veiculo=veiculo, mensagem=mensagem)



if __name__ == "__main__":
    app.run(debug=True)
