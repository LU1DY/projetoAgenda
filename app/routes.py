from app import app, database, bcrypt, admin
from flask import render_template, url_for, request, redirect, flash, jsonify, session
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import FormLogin, FormCriarConta, FormSolicitacao, FormConsulta
from app.models import Usuario, Consulta,Solicitacao
from werkzeug.utils import secure_filename
import os
from datetime import datetime


@app.route("/login", methods=["POST", "GET"])
def login():
    form_login = FormLogin()
    visualizarSenhaLogin = {'js': 'visualizarSenhaLogin.js'}
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario:
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
    return render_template("criarconta.html", form_criar_conta=form_criar_conta, visualizarSenhaCriarConta=visualizarSenhaCriarConta)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/admin')
def admin():
    return redirect(url_for('admin.index'))

@app.route("/", methods=['GET', 'POST'])
def homepage():
    
    if current_user.is_authenticated:

        agora = datetime.now()
        consultas_expiradas = Consulta.query.filter(Consulta.data <= agora).all()
        solicitacoes_experidas = Solicitacao.query.filter(Solicitacao.data <= agora).all()
        for consulta in consultas_expiradas:
            database.session.delete(consulta)
        database.session.commit()
        for solicitacao in solicitacoes_experidas:
            database.session.delete(solicitacao)
        database.session.commit()
        users = Usuario.query.all()
        is_admin = current_user.is_authenticated and getattr(current_user, 'is_admin', False)
        solicitacoesPorUsuario = Solicitacao.query.filter_by(usuario_id=current_user.id).all()
        consultasPorUsuario = Consulta.query.filter_by(usuario_id=current_user.id).all()
        consultas = Consulta.query.all()
        solicitacoes = Solicitacao.query.all()
        datas_agendadas = [consulta.data for consulta in consultas]
        form_solicitacao = FormSolicitacao()
        form_consulta = FormConsulta()
        form_consulta.username.choices = [(usuario.id, usuario.username) for usuario in users]
        if form_solicitacao.validate_on_submit():
            if form_solicitacao.data.data in datas_agendadas:
                flash('Data já agendada, escolha outra!', 'warning')
            else:
                solicitacao = Solicitacao(
                    servico=form_solicitacao.servico.data,
                    motivo=form_solicitacao.motivo.data,
                    data=form_solicitacao.data.data,
                    usuario_id=current_user.id,
                    user_name=current_user.username
                )
                database.session.add(solicitacao)
                database.session.commit()
                flash('Solicitação enviada com sucesso!', 'success')
            return redirect(url_for('homepage'))
        if form_consulta.validate_on_submit():
            consulta = Consulta(
                usuario_id=form_consulta.username.data,
                servico=form_consulta.servico.data,
                data=form_consulta.data.data,
                user_name=Usuario.query.get(form_consulta.username.data).username
            )
            database.session.add(consulta)
            database.session.commit()
            flash('Consulta agendada com sucesso!', 'success')
            return redirect(url_for('homepage'))

        return render_template(
            "homepage.html", 
            admin=is_admin, 
            users=users, 
            form_solicitacao=form_solicitacao, 
            form_consulta=form_consulta, 
            datas_agendadas=datas_agendadas, 
            solicitacoesPorUsuario=solicitacoesPorUsuario,
            solicitacoes=solicitacoes, 
            consultasPorUsuario=consultasPorUsuario, 
            consultas=consultas
        )
    else:
        return render_template('homepage.html')


@app.route('/cancelarConsulta/<int:id>', methods=['POST'])
def cancelarConsulta(id):
    consulta = Consulta.query.get_or_404(id)
    database.session.delete(consulta)
    database.session.commit()
    flash('Consulta cancelada.', 'info')
    return redirect(url_for('homepage'))


@app.route('/cancelarSolicitacao/<int:id>', methods=['POST'])
def cancelarSolicitacao(id):
    solicitacao = Solicitacao.query.get_or_404(id)
    database.session.delete(solicitacao)
    database.session.commit()
    flash('Consulta cancelada.', 'info')
    return redirect(url_for('homepage'))


@app.route('/agenda')
def agenda():
    return render_template('agenda.html')

@app.route('/confirmar/<int:id>', methods=['POST'])
def confirmar(id):
    solicitacao = Solicitacao.query.get_or_404(id)
    consulta = Consulta(
        servico=solicitacao.servico,
        motivo=solicitacao.motivo,
        data=solicitacao.data,
        user_name=solicitacao.user_name,
        usuario_id=solicitacao.usuario_id,
    )
    database.session.add(consulta)
    database.session.delete(solicitacao)
    database.session.commit()
    flash('Solicitação confirmada!', 'success')
    return redirect(url_for('homepage'))

@app.route('/cancelar/<int:id>', methods=['POST'])
def cancelar(id):
    solicitacao = Solicitacao.query.get_or_404(id)
    database.session.delete(solicitacao)
    database.session.commit()
    flash('Solicitação cancelada.', 'info')
    return redirect(url_for('homepage'))


# Rota para promover um usuário a administrador (acessível apenas por outros administradores)
@app.route('/promote', methods=['POST'])
@login_required
def promote():
    if not current_user.is_admin:
        flash('Acesso negado.')
        return redirect(url_for('homepage'))

    user_id = request.form.get('user_id')  # Obtem o ID do usuário
    user = Usuario.query.get(user_id)
    if user:
        user.is_admin = True  # Promove o usuário a administrador
        database.session.commit()
        flash(f'O usuário {user.username} foi promovido a administrador.')
    else:
        flash('Usuário não encontrado.')
    return redirect(url_for('homepage'))


