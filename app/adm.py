from app.models import database, Usuario
from app import app, bcrypt

# Supondo que o app esteja configurado corretamente para o banco de dados
with app.app_context():
    database.create_all()  # Certifique-se de que as tabelas estão criadas
    admin_user = Usuario(username="ADMluidy1", email="luidymichael1@gmail.com", senha=bcrypt.generate_password_hash("2004$5002023Luidy").decode('utf-8'), is_admin=True)
    database.session.add(admin_user)
    database.session.commit()