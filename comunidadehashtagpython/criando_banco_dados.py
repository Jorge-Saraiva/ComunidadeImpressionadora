# Comandos para o Banco de Dados

from main import database
# No arquivo 'main' tem o banco de dados 'database'

from comunidadehashtagpython.models import Usuario, Post
# No arquivo 'models' tem a tabela de 'Usuario' e 'Post'

database.create_all()
# Cria o banco de dados

usuario = Usuario(username='Jorge', email='fenixgaspar@gmail.com', senha='49063235')
usuario2 = Usuario(username='Kassi', email='kassi_pires@gmail.com', senha='123456789')

# usuario = variável para armazenar as informações que queremos da tabela 'Usuario'

database.session.add(usuario)
database.session.add(post1)
# Adiciona em uma pasta temporária esse usuario e/ou post

database.session.commit()
# Salva os usuários que foram adicionados no banco de dados

Usuario.query.all()
# Verifica todos os usuários que têm no banco de dados

Post.query.all()
# Verifica todas as postagens dos usuários que têm no banco de dados

usuario_teste = Usuario.query.first()
# Armazena na variável o primeiro usuário no banco de dados

usuario_teste.email
# Parâmetro para verificar o email do usuario

usuario_kassi = Usuario.query.filter_by(email='kassi_pires@gmail.com').first()
# Cria uma variável do usuario filtrando pelo email, com o parâmetro 'first()' no final

database.drop_all()
# Deleta todo o banco de dados



