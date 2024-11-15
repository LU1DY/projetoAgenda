from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask_admin import Admin

# cria uma instancia do flask admin, que é usada para criar aquele painel administrativo
admin = Admin()

# cria uma instancia do flask, aqui criamos o nosso projeto, mas ainda é um projeto vazio
app = Flask(__name__)

# a SECRET_KEY, é necessária para a segurança dos formulários, adicionamos o hidden_tag() nos formulários para aplicar essa camada de segurança
app.config["SECRET_KEY"] = 'b8605e5bfad413f5b48f79f5a057bb48b9da9c96'

# configura o banco de dados local, usada para interagir com o banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///agendaDB.db'

# cria uma instancia do SQLAlchemy para inicializar o banco de dados
database = SQLAlchemy(app)

# bcrypt é usado como forma de criptografia de senhas
bcrypt = Bcrypt(app)

# importa as rotas do site
from app import routes

# cria uma instancia do login manager para gerenciar o login do usuário
login_manager = LoginManager(app)

# essa estrutura pega o ID do usuário armazenado no banco de dados e usa para redirecionar o usuário para a sua página
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# define a rota de login
login_manager.login_view = 'login'    

# importa os modelos(tabelas) de banco de dados para criar as tabelas
from app.models import Usuario, Consulta

# cria as tabelas
with app.app_context():
    database.create_all() 
