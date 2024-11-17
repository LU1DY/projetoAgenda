from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateTimeLocalField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

# importação do banco de dados, usamos na parte de verificação se o e-mail já foi cadastrado ou não
from app.models import Usuario

# formulário de criar conta
class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    confirmacao = PasswordField('Confirme a senha', validators=[DataRequired(), EqualTo('senha')])
    btn_submit_criar_conta = SubmitField('Criar Conta')


    # verifica se o e-mail informado já foi cadastrado
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise  ValidationError('Email já cadastrado!')

# formulário de login
class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    btn_submit_login = SubmitField('Login')


# formulário de solicitação (disponível apenas para usuários)
class FormSolicitacao(FlaskForm):
    servico = StringField('Nome', validators=[DataRequired()])
    motivo = TextAreaField('Email', validators=[DataRequired()])
    data = DateTimeLocalField('Data da Consulta', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Enviar')


# formulário de consulta (disponível apenas para o ADM)
class FormConsulta(FlaskForm):
    username = SelectField('Selecione um usuário:', validators=[DataRequired()], choices=[])
    servico = StringField('Selecione um serviço: ', validators=[DataRequired()])
    data = DateTimeLocalField('Selecione uma data: ', validators=[DataRequired()])
    submit = SubmitField('Agendar')


# StringField: para campos de texto
# PasswordField: para campos de senha
# DateTimeLocalField: campo para selecionar data e hora. O formato esperado é 'YYYY-MM-DDTHH:MM'
# TextAreaField: também para campos de texto, mas com a diferença de que adiciona uma tag textarea ao invés de um input
# SelectField: adiciona uma tag select, é aquela caixa de seleção para adicionar novo administrador e para adicionar consulta onde escolhemos para qual usuário iremos escolher
# SubmitField: para botões

# VALIDATORS: 
# validators são os parâmetros que adicionamos nos formulários para validar um usuário
# DataRequired(): indica que aquele campo precisa ser preenchido
# Email(): verifica se o dado informado é um email
# Length(8, 20): define o tamanho máximo e mínimo do dado, nesse caso da senha
# EqualTo('senha'): verifica se o campo de confirmação de senha é igual ao campo de senha
