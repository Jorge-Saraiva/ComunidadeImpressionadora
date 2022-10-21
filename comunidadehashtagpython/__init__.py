from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Iniciar o programa (site)
app = Flask(__name__)

# url_for (permite alterar o nome da página, sem necessitar atualizar as outras páginas).

# Gerando um token, para configurarmos a segurança dos nossos formulários
    #1 - Abrir o terminal e escrever 'python'
    #2 - Digitar 'import secrets'
    #3 - Digitar 'secrets.token_hex(16)'
    #4 - Copiar o token gerado e passar no parâmetro:
        #app.config['SECRET_KEY'] = 'token gerado'

app.config['SECRET_KEY'] = '77466cde9f5acfd9034c249a6bac5cca'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
# Criptografar a senha do nosso site
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Caso o usuário não esteja logado, ao tentar acessar uma página ele será redirecionado para a página de login, e após efetuado o login, irá ser redirecionado para a página que estava tentando efetuar o login
login_manager.login_message = 'Favor fazer Login para acessar está página'
login_manager.login_message_category = 'alert-info'

from comunidadehashtagpython import routes









