from app import app, admin, database
from app.models import Usuario, Consulta, Solicitacao
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms.fields import DateTimeLocalField
from flask_admin.form import DateTimePickerWidget
from flask import redirect, url_for

# Formulário para agendar consultas (disponível para o ADM)
class ConsultaForm(FlaskForm):
    # SelectField para selecionar um usuário (coerce=int: converte o ID para inteiro)
    usuario_id = SelectField('Usuário', coerce=int, validators=[DataRequired()])
    data = DateTimeLocalField('Data', validators=[DataRequired()], widget=DateTimePickerWidget())
    servico = StringField('Serviço', validators=[DataRequired()])
    motivo = StringField('Motivo', validators=[DataRequired()])


class SolicitacaoForm(FlaskForm):
    usuario_id = SelectField('Usuário', coerce=int, validators=[DataRequired()])
    data = DateTimeLocalField('Data', validators=[DataRequired()], widget=DateTimePickerWidget())
    servico = StringField('Serviço', validators=[DataRequired()])
    motivo = StringField('Motivo', validators=[DataRequired()])

# Classe personalizada para visualizar e adicionar consultas no painel admin
class ConsultaView(ModelView):
    form = ConsultaForm
    form_overrides = {
        'data': DateTimeLocalField  # sobrepõe o campo data com o tipo DateTimeLocalField
    }
    form_args = {
        'data': {
            'widget': DateTimePickerWidget()  # adiciona o calendário ao campo data
        }
    }

    # Inicializa a consulta no admin
    def __init__(self, session, **kwargs):
        super().__init__(Consulta, session, **kwargs)

    # Preenche o campo select com todos os usuários ao editar uma consulta
    def on_form_prefill(self, form, id):
        form.usuario_id.choices = [(user.id, user.username) for user in Usuario.query.all()]

    # Cria um formulário de consulta com a lista de usuários
    def create_form(self):
        form = super().create_form()
        form.usuario_id.choices = [(user.id, user.username) for user in Usuario.query.all()]
        return form

    # Edita um formulário de consulta com a lista de usuários
    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.usuario_id.choices = [(user.id, user.username) for user in Usuario.query.all()]
        return form

    # Cria um novo registro de consulta no banco de dados
    def create_model(self, form):
        user = Usuario.query.get(form.usuario_id.data)
        if user:
            # Cria uma nova consulta associada ao usuário selecionado
            consulta = Consulta(
                servico=form.servico.data,
                motivo=form.motivo.data,
                data=form.data.data,
                user_name=user.username,
                usuario_id=form.usuario_id.data
            )
            self.session.add(consulta)  # adiciona ao banco de dados
            self.session.commit()  # salva a consulta no banco
            return consulta
        return super().create_model(form)

    # Atualiza o nome do usuário associado à consulta
    def update_model(self, form, model):
        user = Usuario.query.get(form.usuario_id.data)
        if user:
            model.user_name = user.username
        return super().update_model(form, model)

# Classe para adicionar um botão "Voltar para Home" no painel admin
class HomeView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('homepage'))  # redireciona para a página inicial

# Classe personalizada para gerenciar solicitações no painel admin
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

    # Cria um novo registro de solicitação no banco de dados
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
            self.session.add(solicitacao)  # adiciona ao banco
            self.session.commit()  # salva no banco
            return solicitacao
        return super().create_model(form)

    # atualiza o banco de dados de consulta com o id do usuário selecionado
    def update_model(self, form, model):
        user = Usuario.query.get(form.usuario_id.data)
        if user:
            model.user_name = user.username
        return super().update_model(form, model)

# Função que inicializa o painel admin
def init_app(app):
    admin.init_app(app)  # inicializa o painel admin
    admin.add_view(ModelView(Usuario, database.session))  # adiciona a visualização para a tabela Usuario
    admin.add_view(ConsultaView(database.session))  # adiciona a visualização para a tabela Consulta
    admin.add_view(SolicitacaoView(database.session))  # adiciona a visualização para a tabela Solicitacao
    admin.add_view(HomeView(name='Voltar para Home'))  # adiciona botão para voltar à home
