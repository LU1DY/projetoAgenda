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


class SolicitacaoForm(FlaskForm):
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


    def create_model(self, form):
        user = Usuario.query.get(form.usuario_id.data)
        if user:

            consulta = Consulta(
                servico=form.servico.data,
                motivo=form.motivo.data,
                data=form.data.data,
                user_name=user.username, 
                usuario_id=form.usuario_id.data
            )
            self.session.add(consulta)
            self.session.commit()
            return consulta
        return super().create_model(form)

    def update_model(self, form, model):
        user = Usuario.query.get(form.usuario_id.data)
        if user:
            model.user_name = user.username
        return super().update_model(form, model)

class HomeView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('homepage')) 

class SolicitacaoView(ModelView):
    form = SolicitacaoForm

    column_list = ['id', 'user_name', 'servico', 'motivo', 'data', 'usuario_id']

    def __init__(self, session, **kwargs):
        super().__init__(Solicitacao, session, **kwargs)

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

    def create_model(self, form):
        user = Usuario.query.get(form.usuario_id.data)
        if user:
            solicitacao = Solicitacao(
                servico=form.servico.data,
                motivo=form.motivo.data,
                data=form.data.data,
                usuario_id=form.usuario_id.data,
                user_name=user.username
            )
            self.session.add(solicitacao)
            self.session.commit()
            return solicitacao
        return super().create_model(form)

    def update_model(self, form, model):
        user = Usuario.query.get(form.usuario_id.data)
        if user:
            model.user_name = user.username
        return super().update_model(form, model)

def init_app(app):
    admin.init_app(app)
    admin.add_view(ModelView(Usuario, database.session))
    admin.add_view(ConsultaView(database.session))
    admin.add_view(SolicitacaoView(database.session))
    admin.add_view(HomeView(name='Voltar para Home'))
