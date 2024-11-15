from app import database
from flask_login import UserMixin

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(50), nullable=False, unique=True)
    email = database.Column(database.String(120), nullable=False, unique=True)
    senha = database.Column(database.String(200), nullable=False)
    is_admin = database.Column(database.Boolean, default=False)
    consultas = database.relationship('Consulta', back_populates='usuario', lazy=True)



class Solicitacao(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    servico = database.Column(database.String(50), nullable=False)
    motivo = database.Column(database.String(120))
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    data = database.Column(database.DateTime, nullable=False)
    user_name = database.Column(database.String(50), database.ForeignKey('usuario.username'), nullable=False)


class Consulta(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    servico = database.Column(database.String(50), nullable=False)
    motivo = database.Column(database.String(120))
    data = database.Column(database.DateTime, nullable=False) 
    user_name = database.Column(database.String, nullable=False)
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    usuario = database.relationship('Usuario', back_populates='consultas')
