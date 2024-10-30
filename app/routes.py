from app import app, database, bcrypt, admin
from flask import render_template, url_for, request, redirect, flash, jsonify, session
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import FormLogin, FormCriarConta
from app.models import Usuario
from werkzeug.utils import secure_filename
import os



@app.route("/login", methods=["POST", "GET"])
def login():
    form_login = FormLogin()
    visualizarSenhaLogin = {'js': 'visualizarSenhaLogin.js'}
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario:
            # Usa bcrypt para verificar a senha
            if bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
                login_user(usuario)
                par_next = request.args.get('next')
                return redirect(par_next) if par_next else redirect(url_for('homepage'))
            else:
                flash('Senha incorreta!')
        else:
            flash(f'Nenhuma conta associada ao e-mail: {form_login.email.data}', 'alert-danger')

    return render_template("login.html", form_login=form_login, visualizarSenhaLogin=visualizarSenhaLogin)


@app.route('/criarconta', methods=["POST", "GET"])
def criarconta():
    form_criar_conta = FormCriarConta()
    visualizarSenhaCriarConta = {'js': 'visualizarSenhaCriarConta.js'}
    if form_criar_conta.validate_on_submit():
        senha_bcrypt = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode('utf-8')
        usuario = Usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data,
                          senha=senha_bcrypt)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario)
        return redirect(url_for('homepage'))
    else:
        flash('Algo deu errado, verifique suas informações e tente novamente.')

    return render_template("criarconta.html", form_criar_conta=form_criar_conta, visualizarSenhaCriarConta=visualizarSenhaCriarConta)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/admin')
@login_required
def admin():
    return


@app.route("/")
def homepage():
    users = Usuario.query.all()  # Busca todos os usuários no banco de dados
    is_admin = current_user.is_authenticated and current_user.is_admin  # Verifica se o usuário está autenticado e se é o ADM
    return render_template("homepage.html", admin=is_admin, users=users)

@app.route('/agenda')
def agenda():
    return render_template('agenda.html')

# Rota para promover um usuário a administrador (acessível apenas por outros administradores)
@app.route('/promote', methods=['POST'])
@login_required
def promote():
    if not current_user.is_admin:
        flash('Acesso negado.')
        return redirect(url_for('homepage'))

    user_id = request.form.get('user_id')  # Obtenha o ID do usuário do formulário
    user = Usuario.query.get(user_id)
    if user:
        user.is_admin = True  # Promova o usuário a administrador
        database.session.commit()
        flash(f'O usuário {user.username} foi promovido a administrador.')
    else:
        flash('Usuário não encontrado.')
    return redirect(url_for('homepage'))