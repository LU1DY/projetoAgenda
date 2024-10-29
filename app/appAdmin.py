from app import app, admin, database
from app.models import Usuario, Produtos
from flask_admin.contrib.sqla import ModelView


def init_app(app):
    app.config['SECRET_KEY'] = 'K9#hS8vJ2xF!mQ3u@L7^tR6gB$eY5kP1jH8*zU4w9F3o'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agenda.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    if app.debug:
        app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
        app.config['DEBUG_TB_PROFILER_ENABLED'] = True

    admin.init_app(app)
    admin.add_view(ModelView(Usuario, database.session))
    admin.add_view(ModelView(Produtos, database.session))


