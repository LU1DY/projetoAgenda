from app import database
from flask_login import UserMixin

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    is_admin = database.Column(database.Boolean, default=False)


class Produtos(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nameProduct = database.Column(database.String, nullable=False)
    descriptionProduct = database.Column(database.String, nullable=False)
    price = database.Column(database.Integer, nullable=False)
    

class Evento(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    data_inicio = database.Column(database.Date, nullable=False)
    data_fim = database.Column(database.Date, nullable=True)