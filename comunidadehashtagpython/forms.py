from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadehashtagpython.models import Usuario, Post
from flask_login import current_user


# Criando formulários

#FlaskForm = Formulário Flask (Python)
#FileFiled = Permite ao Usuário escolher um arquivo no computador (passar o parâmetro 'enctype="multipart/form-data"' no 'form' - campo do formulário - do HTML)
#FileAllowed = Validador de extensões de arquivos
#StringField = Campo de Texto
#PasswordField = Campo de Senha
#SubmitField = Campo de botao (envio formulário)
#BooleanField() = Lembrar dados
#DataRequired() = Campo OBRIGATÓRIO
#Length(x, y) = Tamanho de algum campo (x=minimo, y=maximo)
#Email() = Define o campo como sendo de E-mail (verificando a presença de @ e .) -
#EqualTo('senha') = Verifica se a CONFIRMAÇÃO DE SENHA é igual a SENHA


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(message="Digite um nome de usuário válido")])
    email = StringField('Email', validators=[DataRequired(), Email(message='Digite um e-mail válido')])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(4, 20)])
    confirmacao = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha', message='as senhas não coincidem')])
    botao_submit_criar_conta = SubmitField('Criar Conta')

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Nome de Usuário já cadastrado. Cadastre-se com outro Nome de Usuário para continuar')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')

    def validate_senha(self, senha):
        senha = Usuario.query.filter_by(senha=senha.data).first()
        if senha:
            raise ValidationError('Digite uma senha entre 4 e 20 caracteres')


class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Digite um e-mail válido')])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(4, 20, message='Digite um valor para a senha entre 4 e 20 caracteres')])
    lembrar_dados = BooleanField('Lembrar dados de Acesso')
    botao_submit_login = SubmitField('Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message='Digite um e-mail válido')])
    # Adicionando arquivos foto no site, validando para as extensões informadas
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg'],message="Somente arquivos com extensões: jpg, jpeg e png")])
    # Criar campos com cursos
    curso_ppt = BooleanField('Apresentações Impressionadoras')
    curso_autocad = BooleanField('Autocad')
    curso_excel = BooleanField('Excel Impressionador')
    curso_javascript = BooleanField('JavaScript')
    curso_outlook = BooleanField('Outlook')
    curso_photoshop = BooleanField('Photoshop')
    curso_php = BooleanField('PHP')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_revit = BooleanField('Revit')
    curso_sql = BooleanField('SQL Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_word = BooleanField('Word')

    botao_submit_editar_perfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        # verificar se houve alteração de e-mail
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com este E-mail. Cadastre-se com outro e-mail')

    def validate_username(self, username):
        # verificar se houve alteração de usuario
        if current_user.username != username.data:
            usuario = Usuario.query.filter_by(username=username.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com este username. Altere o username para continuar')


class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')




# csrf token = Cria um campo de segurança na parte interna do site, para evitar ataques maliciosos no site/banco de dados, etc
