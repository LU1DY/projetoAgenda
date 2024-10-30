from app.models import database, Usuario
from app import app, bcrypt

with app.app_context():
    database.create_all()  #cria as tabelas
# Cria um usuário administrador com base nos dados
    admin_user = Usuario(username="ADMluidy1", email="luidy@gmail.com", senha=bcrypt.generate_password_hash("5002023Luidy").decode('utf-8'), is_admin=True)
    database.session.add(admin_user)
    database.session.commit()