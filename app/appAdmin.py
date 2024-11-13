from app import app, admin, database
from app.models import Usuario, Consulta, Solicitacao
from flask_admin import Admin,  BaseView, expose
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms.fields import DateTimeLocalField
from flask_admin.form import DateTimePickerWidget
from flask import redirect, url_for

class ConsultaForm(FlaskForm):
    usuario_id = SelectField('Usuário', coerce=int, validators=[DataRequired()])
    data = DateTimeLocalField('Data', validators=[DataRequired()], widget=DateTimePickerWidget())
    servico = StringField('Serviço', validators=[DataRequired()])
    motivo = StringField('Motivo', validators=[DataRequired()])



class ConsultaView(ModelView):
    form_overrides = {
        'data': DateTimeLocalField
    }

    form_args = {
        'data': {
            'widget': DateTimePickerWidget()
        }
    }

    form = ConsultaForm

    def __init__(self, session, **kwargs):
        super().__init__(Consulta, session, **kwargs)

    def on_form_prefill(self, form, id):
        form.usuario_id.choices = [(user.id, user.username) for user in Usuario.query.all()]

    def create_form(self):
        form = super().create_form()
        form.usuario_id.choices = [(user.id, user.username) for user in Usuario.query.all()]
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.usuario_id.choices = [(user.id, user.username) for user in Usuario.query.all()]
        return form

class HomeView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('homepage'))  # Redireciona para a homepage


def init_app(app):
    app.config['SECRET_KEY'] = 'K9#hS8vJ2xF!mQ3u@L7^tR6gB$eY5kP1jH8*zU4w9F3o'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_TEMPLATE_MODE'] = 'bootstrap4'

    admin.init_app(app)
    admin.add_view(ModelView(Usuario, database.session))
    admin.add_view(ModelView(Solicitacao, database.session))
    admin.add_view(ConsultaView(database.session))
    admin.add_view(HomeView(name='Voltar para Home'))  # Adiciona o link de retorno para a homepage

