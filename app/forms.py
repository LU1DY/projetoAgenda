from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateTimeLocalField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models import Usuario

# formulário de criar conta
class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    confirmacao = PasswordField('Confirme a senha', validators=[DataRequired(), EqualTo('senha')])
    btn_submit_criar_conta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise  ValidationError('Email já cadastrado!')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    btn_submit_login = SubmitField('Login')


class FormSolicitacao(FlaskForm):
    servico = StringField('Nome', validators=[DataRequired()])
    motivo = TextAreaField('Email', validators=[DataRequired()])
    data = DateTimeLocalField('Data da Consulta', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Enviar')


class FormConsulta(FlaskForm):
    username = SelectField('Selecione um usuário:', validators=[DataRequired()], choices=[])
    servico = StringField('Selecione um serviço: ', validators=[DataRequired()])
    data = DateTimeLocalField('Selecione uma data: ', validators=[DataRequired()])
    submit = SubmitField('Agendar')