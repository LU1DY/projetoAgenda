from app.models import Usuario
from app import app, bcrypt, database

with app.app_context():
    database.create_all()  #cria as tabelas
    # Cria um usuário administrador com base nos dados necessários especificados no banco de dados
    admin_user = Usuario(username="adm", email="adm@gmail.com", senha=bcrypt.generate_password_hash("admadmadm").decode('utf-8'), is_admin=True)
    
    database.session.add(admin_user)
    database.session.commit()
