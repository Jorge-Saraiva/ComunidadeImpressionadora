from flask import render_template, redirect, request, url_for, flash, abort
from comunidadehashtagpython import app, database, bcrypt
from comunidadehashtagpython.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidadehashtagpython.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


# Criando funções de páginas
@app.route("/")  # informar qual o link que será a homepage
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)  # linka a minha página html com o Flask

@app.route("/contato")  # informar qual o link que será a homepage
def contato():
    return render_template('contato.html')

@app.route("/usuarios")  # informar qual o link que será a homepage
@login_required  # Bloqueia a página, para evitar que pessoas não logadas possam visualizar os dados
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route("/login", methods=['GET', 'POST']) # Libera para o usuário enviar informações para o site
def login():
    form_login = FormLogin()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        # Permissão login (verificar se usuário existe e se a senha está correta)
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            # Exibir mensagem de login bem sucedido
            flash(f'Login realizado com sucesso para o e-mail: {form_login.email.data}', 'alert-success')
            # Verificar se o usuário está tentando acessar alguma página que só é possível, quando está logado
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                # Redirecionar para a Home Page
                return redirect(url_for('home'))
        else:
            flash(f'Falha no Login. E-mail e/ou Senha incorretos', 'alert-danger')
        return redirect(url_for('login'))
    return render_template('login.html', form_login=form_login)

@app.route("/criarconta", methods=['GET', 'POST']) # Libera para o usuário enviar informações para o site
def criarconta():
    form_criar_conta = FormCriarConta()

    if form_criar_conta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        # Criptografar senha
        senha_cript = bcrypt.generate_password_hash(form_criar_conta.senha.data)
        # Criar o usuario
        usuario = Usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data, senha=senha_cript)
        # Adicionar a sessão
        database.session.add(usuario)
        # Commit
        database.session.commit()
        flash(f'Conta criada com sucesso para o e-mail: {form_criar_conta.email.data}', 'alert-success')
        return redirect(url_for('login'))
    return render_template('criarconta.html', form_criar_conta=form_criar_conta)

@app.route("/sair")
@login_required  # Bloqueia a página, para evitar que pessoas não logadas possam visualizar os dados
def sair():
    logout_user()
    flash(f'Logout realizado com Sucesso', 'alert-success')
    return redirect(url_for("home"))

@app.route("/perfil")
@login_required  # Bloqueia a página, para evitar que pessoas não logadas possam visualizar os dados
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template("perfil.html", foto_perfil=foto_perfil)

@app.route("/post/criar", methods=['GET', 'POST'])
@login_required  # Bloqueia a página, para evitar que pessoas não logadas possam visualizar os dados
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template("criarpost.html", form=form)


def salvar_imagem(imagem):
    # Adicionar um código aleatório no nome da imagem
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = os.path.join(nome + codigo + extensao)
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    # Reduzir o tamanho da imagem
    tamanho = (600, 600)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # Salvar a foto na pasta de Perfil
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


# Criar uma função, para percorrer os campos do formulário, para verificar os cursos selecionados
def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            # Adicionar o texto do campo.label ('Excel Impressionador') na lista de cursos
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)


@app.route("/perfil/editar", methods=['GET', 'POST'])
@login_required  # Bloqueia a página, para evitar que pessoas não logadas possam visualizar os dados
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash(f'Perfil atualizado com Sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":  # Carregar informações com auto preenchimento dos campos de e-mail e username
        form.email.data = current_user.email
        form.username.data = current_user.username
    if 'Apresentações Impressionadoras' in current_user.cursos:
        form.curso_ppt.data = current_user.cursos
    if 'Excel Impressionador' in current_user.cursos:
        form.curso_excel.data = current_user.cursos
    if 'Power BI Impressionador' in current_user.cursos:
        form.curso_powerbi.data = current_user.cursos
    if 'Python Impressionador' in current_user.cursos:
        form.curso_python.data = current_user.cursos
    if 'SQL Impressionador' in current_user.cursos:
        form.curso_sql.data = current_user.cursos
    if 'VBA Impressionador' in current_user.cursos:
        form.curso_vba.data = current_user.cursos
    if 'Autocad' in current_user.cursos:
        form.curso_autocad.data = current_user.cursos
    if 'JavaScript' in current_user.cursos:
        form.curso_javascript.data = current_user.cursos
    if 'Outlook' in current_user.cursos:
        form.curso_outlook.data = current_user.cursos
    if 'Photoshop' in current_user.cursos:
        form.curso_photoshop.data = current_user.cursos
    if 'PHP' in current_user.cursos:
        form.curso_php.data = current_user.cursos
    if 'Revit' in current_user.cursos:
        form.curso_revit.data = current_user.cursos
    if 'Word' in current_user.cursos:
        form.curso_word.data = current_user.cursos

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template("editarperfil.html", foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required  # Bloqueia a página, para evitar que pessoas não logadas possam visualizar os dados
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com sucesso', 'alert-success')
            return redirect(url_for('home'))
        # Lógica editar post
    else:
        form = None
    return render_template("post.html", post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluído com sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)


@app.route("/perfil/editar/", methods=['GET', 'POST'])
@login_required  # Bloqueia a página, para evitar que pessoas não logadas possam visualizar os dados
def excluir_conta():
    usuario = Usuario.query.filter_by(email=current_user.email).first()
    if current_user.email == usuario.email:
        usuario_post = Post.query.filter_by(id_usuario=current_user.id)
        for post in usuario_post:
            database.session.delete(usuario_post.first())
        database.session.delete(usuario)
        database.session.commit()
        logout_user()
        flash('Perfil excluído com sucesso', 'alert-danger')
        return redirect(url_for('login'))




# form_login.email.data = Pega a informação do email que o usuario preencheu
# bcrypt.generate_password_hash() = transforma a senha do usuário em uma senha criptografada

# Verificar se a senha criptografada é igual a senha passada pelo usuario
""""
Ex.
senha = '49063235'
senha_crypt = bcrypt.generate_password_hash(senha)
senha_crypt
b'$2b$12$tN6Jap4o1lIvR0ii.6oimuptPuXb3mS20AQ7o49AikQi1wJEOmPvO'

Verificando se são iguais
bcrypt.check_password_hash(senha_crypt, senha)
True
"""
