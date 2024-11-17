# importa a instância do banco de daods que criamos no arquivo __init__ (arquivo de confirguração)
from app import database
from flask_login import UserMixin

# define a tebela de usuários no banco de dados
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(50), nullable=False, unique=True)
    email = database.Column(database.String(120), nullable=False, unique=True)
    senha = database.Column(database.String(200), nullable=False)
    is_admin = database.Column(database.Boolean, default=False)
    consultas = database.relationship('Consulta', back_populates='usuario', lazy=True)


# define a tabela de solicitações no banco de dados
class Solicitacao(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    servico = database.Column(database.String(50), nullable=False)
    motivo = database.Column(database.String(120))
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    data = database.Column(database.DateTime, nullable=False)
    user_name = database.Column(database.String(50), database.ForeignKey('usuario.username'), nullable=False)


# define a tabela de consultas no banco de dados
class Consulta(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    servico = database.Column(database.String(50), nullable=False)
    motivo = database.Column(database.String(120))
    data = database.Column(database.DateTime, nullable=False) 
    user_name = database.Column(database.String, nullable=False)
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    usuario = database.relationship('Usuario', back_populates='consultas')



# database.Integer: define que o dado armazenado é do tipo inteiro
# database.String(50): define que o dado armazenado é do tipo string (texto) e que deve ser no máximo 50 caracteres
# database.DateTime: define que o dado armazenado deve ser em formato de data. O formato esperado é 'YYYY-MM-DDTHH:MM'

# primary_key: define que o dado informado é a chave primária dos dados do usuário
# unique=True: define que o dado informado deve ser único no banco de dados, se uma vez informado por um usuário, jamais poderá ser usado por outro
# nullable=False: define que esse campo não pode ficar vazio

# database.relationship: define uma relação entre duas tabelas
# lazy=True: define que o dado da relação só será puxado quando necessário
# back_populates: define uma relação entre duas tabelas, exemplo: database.relationship('Usuario', back_populates='consultas'), o usuário é a tabela que estamos nos relacionando e o consultas é a tabela que precisará do dado da tabela usuário


# usuario_id = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
# a relação entre a tabela de consulta e usuários é necessária para que possamos armazenar o ID do usuário que solicitou/marcamos uma consulta, já que o ID é um dado único de cada usuário, então na linha acima definimos que o dado "usuario_id" armazenará o dado puxado por essa relação: ForeignKey('usuario.id')