import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, get_flashed_messages
from db.conexao import conectar as obter_conexao
from services.veiculo_service import cadastrar_veiculo, buscar_veiculos_por_texto, remover_veiculo, buscar_por_id, buscar_veiculo_exato, atualizar_veiculo, gerar_relatorio, buscar_categorias
from functools import wraps
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = "algumasecretkey"

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'img', 'carros')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
MAX_CONTENT_LENGTH = 4 * 1024 * 1024  # 4 MB limite opcional

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# cria a pasta se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_obrigatorio(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario" not in session:
            flash("Você precisa fazer login para acessar essa página.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_user():
    return dict(session=session)

@app.route('/')
def index():
    return redirect(url_for("tela_inicial"))

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
            cursor = conexao.cursor(dictionary=True)

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
                session["usuario"] = {
                    "id": usuario["id_usuario"],
                    "nome": usuario["nome"]
                }
                return redirect(url_for("tela_inicial"))
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
    session.pop("usuario", None)
    return redirect(url_for("login"))

@app.route("/telaInicial", methods=["GET", "POST"])
def tela_inicial():
    nome_usuario = session["usuario"]["nome"] if "usuario" in session else None

    if request.method == "POST":
        termo_pesquisa = request.form.get("pesquisa", "").strip()

        if termo_pesquisa:
            try:
                conexao = obter_conexao()
                cursor = conexao.cursor(dictionary=True)

                cursor.execute("""
                    SELECT v.*, m.nome AS marca
                    FROM veiculos v
                    JOIN marcas m ON v.id_marca = m.id_marca
                    WHERE LOWER(v.modelo) LIKE LOWER(%s)
                """, (f"%{termo_pesquisa}%",))

                resultado = cursor.fetchone()

                # Se encontrou um carro → redireciona para a tela por marca
                if resultado:
                    marca = resultado["marca"]
                    modelo = resultado["modelo"]
                    return redirect(url_for("carros_por_marca", marca=marca, modelo=modelo))

                else:
                    flash("Nenhum carro encontrado com esse nome.")

            except Exception as e:
                flash(f"Erro ao pesquisar: {e}")

    return render_template("telaInicial.html", nome_usuario=nome_usuario)


@app.route('/adicionar', methods=['GET', 'POST'])
@login_obrigatorio
def adicionar_veiculo():

    get_flashed_messages()
    
    if request.method == 'POST':
        modelo = request.form['modelo']
        marca = request.form['marca']
        ano = int(request.form['ano'])
        preco = float(request.form['preco'])

        categoria_id = request.form.get('categoria')  

        if not categoria_id:
            categorias_selecionadas = request.form.getlist('categorias')
            if categorias_selecionadas:
                categoria_id = categorias_selecionadas[0]


        if not categoria_id or categoria_id == "":
            categoria_id = None
        else:
            categoria_id = int(categoria_id)

        imagem = request.files.get('imagem')
        imagem_url = None

        if imagem and imagem.filename != '':
            if allowed_file(imagem.filename):
                filename = secure_filename(imagem.filename)
                timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
                filename = f"{timestamp}_{filename}"
                caminho_abs = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                imagem.save(caminho_abs)
                imagem_url = f"/static/img/carros/{filename}"
            else:
                flash("Formato de imagem não permitido.")
                return redirect(url_for('adicionar_veiculo'))
        
        id_usuario = session["usuario"]["id"]
        id_marca = buscar_id_marca(marca)

        try:
            cadastrar_veiculo(
                id_usuario, id_marca, ano, modelo, preco,
                imagem_url, categoria_id
            )
            flash("Veículo cadastrado com sucesso!", "adicionar")
        except Exception as e:
            flash(f"Erro ao cadastrar veículo: {e}")
            
        return redirect(url_for('adicionar_veiculo'))
    
    categorias = buscar_categorias()
    return render_template('adicionar.html', categorias=categorias)

def buscar_id_marca(nome_marca):

    conexao = obter_conexao()
    cursor = conexao.cursor(buffered=True)

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
@login_obrigatorio
def remover():
    pesquisa = request.form.get("pesquisa", "")
    resultados = []

    if request.method == "POST" and request.form.get("acao") == "pesquisar":
        resultados = buscar_veiculos_por_texto(pesquisa)

    return render_template("remover.html",
                           resultados=resultados,
                           pesquisa=pesquisa)


@app.route('/confirmar-remocao/<int:id_veiculo>')
@login_obrigatorio
def confirmar_remocao(id_veiculo):
    veiculo = buscar_por_id(id_veiculo)
    if not veiculo:
        flash("Veículo não encontrado.")
        return redirect(url_for("remover"))
    return render_template("confirmar_remocao.html", carro=veiculo)


@app.route('/remover/<int:id_veiculo>', methods=['POST'])
@login_obrigatorio
def remover_final(id_veiculo):
    remover_veiculo(id_veiculo)
    flash("Veículo removido com sucesso!", "remover")
    return redirect(url_for("remover"))

@app.route("/editar", methods=["GET", "POST"])
@login_obrigatorio
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
            categoria_id = request.form.get("categoria")

            # busca o carro atual para remover imagem antiga
            veiculo = buscar_por_id(id_veiculo)

            nova_imagem = request.files.get("imagem")
            imagem_url = veiculo["imagem_url"]

            # --- TRATAR IMAGEM ---
            if nova_imagem and nova_imagem.filename != "":
                if allowed_file(nova_imagem.filename):

                    # APAGAR IMAGEM ANTIGA
                    if veiculo["imagem_url"]:
                        try:
                            caminho_antigo = veiculo["imagem_url"].lstrip("/")
                            os.remove(os.path.join(app.root_path, caminho_antigo))
                        except:
                            pass

                    # SALVAR NOVA
                    nome_arquivo = secure_filename(nova_imagem.filename)
                    caminho = os.path.join("static/img/carros", nome_arquivo)
                    nova_imagem.save(os.path.join(app.root_path, caminho))

                    imagem_url = "/" + caminho

            # Atualizar no BD (novo parâmetro categoria)
            atualizar_veiculo(
                id_veiculo, modelo, marca, ano, preco, imagem_url, categoria_id
            )

            mensagem = "Veículo atualizado com sucesso!"

            veiculo = buscar_por_id(id_veiculo)

    # Sempre buscar categorias para o SELECT no HTML
    categorias = buscar_categorias()

    return render_template(
        "editar.html",
        veiculo=veiculo,
        mensagem=mensagem,
        categorias=categorias
    )


@app.route('/relatorio', methods=['GET', 'POST'])
@login_obrigatorio
def relatorio():
    dados = None

    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT DISTINCT m.nome 
        FROM marcas m
        JOIN veiculos v ON v.id_marca = m.id_marca
        ORDER BY m.nome ASC
    """)
    
    marcas = [row[0] for row in cursor.fetchall()]

    if request.method == "POST":
        marca = request.form.get("marca", "")
        ano_min = request.form.get("ano_min", "")
        ano_max = request.form.get("ano_max", "")
        preco_max = request.form.get("preco_max", "")

        filtros = {
            "marca": marca if marca else None,
            "ano_min": int(ano_min) if ano_min else None,
            "ano_max": int(ano_max) if ano_max else None,
            "preco_max": float(preco_max) if preco_max else None
        }

        try:
            dados = gerar_relatorio(filtros)
        except Exception as e:
            flash(f"Erro ao gerar relatório: {e}", category="relatorio")

    return render_template("relatorio.html", dados=dados, marcas=marcas)

@app.route('/carros/<marca>', methods=['GET'])
@login_obrigatorio
def carros_por_marca(marca):

    modelo_filtro = request.args.get("modelo")  # ← Filtro opcional

    try:
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT v.*, c.nome AS categoria
            FROM veiculos v
            JOIN marcas m ON v.id_marca = m.id_marca
            LEFT JOIN categorias c ON v.id_categoria = c.id_categoria
            WHERE LOWER(m.nome) = LOWER(%s)
        """

        params = [marca]

        if modelo_filtro:
            sql += " AND LOWER(v.modelo) LIKE LOWER(%s)"
            params.append(f"%{modelo_filtro}%")

        cursor.execute(sql, params)
        carros = cursor.fetchall()

        if not carros:
            flash("Nenhum carro encontrado com esse modelo para essa marca.")

        return render_template("carrosPorMarca.html", marca=marca, carros=carros, modelo=modelo_filtro)

    except Exception as e:
        flash(f"Erro ao buscar carros: {e}")
        return redirect(url_for("tela_inicial"))

    finally:
        cursor.close()
        conexao.close()

@app.before_request
def limpar_sessao_em_rotas_especificas():
    rotas_limpar = ["/adicionar", "/editar", "/remover", "/relatorio"]

    # só limpa se for uma dessas rotas
    if request.path in rotas_limpar and "sessao_limpa" not in session:
        session.clear()
        session["sessao_limpa"] = True


if __name__ == "__main__":
    app.run(debug=True)
