from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask_admin import Admin

admin = Admin()


app = Flask(__name__)


app.config["SECRET_KEY"] = 'b8605e5bfad413f5b48f79f5a057bb48b9da9c96'
if os.getenv("SQLALCHEMY_DATABASE_URI"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///agendaDB.db'


database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from app import routes
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

login_manager.login_view = 'login'  # Define a rota de login
login_manager.login_message_category = 'info'  # Categoria das mensagens de alerta


from app.models import Usuario

with app.app_context():
    database.create_all()  # Isso cria as tabelas novamente


