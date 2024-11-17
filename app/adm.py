from app.models import database, Usuario
from app import app, bcrypt

with app.app_context():
    database.create_all()  #cria as tabelas
    # Cria um usuário administrador com base nos dados necessários especificados no banco de dados
    admin_user = Usuario(username="ADM1", email="ADM1@gmail.com", senha=bcrypt.generate_password_hash("amdadmadm").decode('utf-8'), is_admin=True)
    
    database.session.add(admin_user)
    database.session.commit()
