from app import app, database, bcrypt, admin
from flask import render_template, url_for, request, redirect, flash, jsonify, session
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import FormLogin, FormCriarConta, FormSolicitacao, FormConsulta
from app.models import Usuario, Consulta,Solicitacao
from werkzeug.utils import secure_filename
import os
from datetime import datetime

# rota de login e métodos de puxar e mandar dados ao banco de dadso
@app.route("/login", methods=["POST", "GET"])
# função de login
def login():
    # cria uma instância do formulário de login criado no arquivo forms.py
    form_login = FormLogin()
    # armazena o caminho do arquivo de vizualizar senha
    visualizarSenhaLogin = {'js': 'visualizarSenhaLogin.js'}
    # verifica se os dados informados pelo usuário são válidos
    if form_login.validate_on_submit():
        # se for válidado, ele procura se o usuário existe e-mail no banco de dados
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        # se o usuário existe
        if usuario:
            # ele pega a senha do usuário, descriptografa a senha e compara se a senha informada é igual a senha informada na hora do cadastro
            if bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
                login_user(usuario)
                par_next = request.args.get('next')
                # se tudo der certo, redireciona o usuário para a homepage
                return redirect(par_next) if par_next else redirect(url_for('homepage'))
            else:
                # caso e senha não for informada corretamente retorna a mensagem
                flash('Senha incorreta!')
        else:
            # se o e-mail buscado não for encontrado, retorna que o email informado não esta associado a nenhuma conta
            flash(f'Nenhuma conta associada ao e-mail: {form_login.email.data}', 'alert-danger')
    # retorna a página de login, a instância criada do formulário para adicionarmos os inputs de formulário e o caminho do arquivo javascript para visualizar senha
    return render_template("login.html", form_login=form_login, visualizarSenhaLogin=visualizarSenhaLogin)

# rota para página de criar conta e adiciona os métodos de postar e puxar dados do banco de dados
@app.route('/criarconta', methods=["POST", "GET"])
def criarconta():
    # cria uma instância do formulário de criar conta criado no arquivo forms.py
    form_criar_conta = FormCriarConta()
    # armazena o caminho do arquivo de vizualizar senha
    visualizarSenhaCriarConta = {'js': 'visualizarSenhaCriarConta.js'}
    # verifica se os dados informados pelo usuário são válidos
    if form_criar_conta.validate_on_submit():
        # se forem válidos ele pega a senha informada e criptografa para armazenar no banco de dados criptografada (exemplo de senha criptografada: senha sem criptografia: amdadmadm, criptografada: $2b$12$nSOpcuFhF7yxCctcR16WFupaYINmE/0MXuEMsi5o4WbN4n2pBdvW2)
        senha_bcrypt = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode('utf-8')
        # após criptografar, cria um novo usuário armazenando os dados exigidos pelo banco de dados
        usuario = Usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data,
                          senha=senha_bcrypt)
        # adiciona o usuário ao banco de dados
        database.session.add(usuario)
        # salva o usuário
        database.session.commit()
        # cria o usuário já logando ele no sistema, não havendo necessiadade do usuário se cadastra e logar novamente
        login_user(usuario)
        # redireciona o usuário para a homepage
        return redirect(url_for('homepage'))
    # retorna o template de criar conta, a instância de criar conta e o caminho do arquivo de visualizar senha
    # o último return nçao depende de validações, independentemente do reusltado do if, ele retorna os dados na linha abaixo
    return render_template("criarconta.html", form_criar_conta=form_criar_conta, visualizarSenhaCriarConta=visualizarSenhaCriarConta)

# rota para logout (não há template, tecnicamnte a rota não existe, mas é necessário atribuir a função a uma rota)
@app.route('/logout')
# apenas usuário logados no sistema tem acesso a essa função
@login_required
def logout():
    # faz a função de deslogar o usuário do sistema
    logout_user()
    # retorna o usuário para a homepage, mas, com funções diferentes (o sistma roda em torno da homepage, mas há verificações que retornam diferentes funções para a homepage, como se o usuário esta logado ou não ou se é um ADM ou usuário comum)
    return redirect(url_for('homepage'))

# rota para o painel de administrador
@app.route('/admin')
def admin():
    # retorna o que seria o template html do painel, é necessário adicionar já que estamos atribuindo essa rpta a um botão da barra de navegação de ADM, mas o panel de ADM é gerado automaticamente quando configuramos o admin no arquivo __init__ e appAdmin
    return redirect(url_for('admin.index'))

# rota de homepage e métodos que permitem envio e requisições de dados ao banco de dados 
@app.route("/", methods=['GET', 'POST'])
def homepage():
    # verifica se o usuário atual esta logado
    if current_user.is_authenticated:
        # se sim, ele pega a data e hora atual
        agora = datetime.now()
        # verifica se há alguma consulta agendada para o horário atual
        consultas_expiradas = Consulta.query.filter(Consulta.data <= agora).all()
        # verifica se há alguma solicitação agendada para o horário atual
        solicitacoes_experidas = Solicitacao.query.filter(Solicitacao.data <= agora).all()
        # se houver alguma consulta para a data atual ou se huover alguma consulta que já expirou ele apaga do banco de dados
        for consulta in consultas_expiradas:
            database.session.delete(consulta)
        database.session.commit()
        # se houver alguma solicitação para a data atual ou se huover alguma consulta que já expirou ele apaga do banco de dados
        for solicitacao in solicitacoes_experidas:
            database.session.delete(solicitacao)
        database.session.commit()
        # armazena todos os usuários do banco de dados
        users = Usuario.query.all()
        # verifica se o usuário atual esta logado e se há algum atributo 'is_admin'(que é o atributo que define um usuário como administrador), se houver ele armazena o valor True na váriavel "is_admin", se não houver ele armazena 'False'
        is_admin = current_user.is_authenticated and getattr(current_user, 'is_admin', False)
        # armazena todas as solicitações do usuário
        solicitacoesPorUsuario = Solicitacao.query.filter_by(usuario_id=current_user.id).all()
        # armazena todas as consultas do usuário
        consultasPorUsuario = Consulta.query.filter_by(usuario_id=current_user.id).all()
        # armazena todas as consultas do banco de dados
        consultas = Consulta.query.all()
        # armazena todas as solicitações do banco de dados
        solicitacoes = Solicitacao.query.all()
        # armazena todas as datas já agendadas do banco de dados
        datas_agendadas = [consulta.data for consulta in consultas]
        # cria uma instancia do formulário de solicitação 
        form_solicitacao = FormSolicitacao()
        # cria uma instancia do formulário de consulta 
        form_consulta = FormConsulta()
        # armazena o nome e o id de cada usuário
        form_consulta.username.choices = [(usuario.id, usuario.username) for usuario in users]
        # verifica se os dados informados são válidos
        if form_solicitacao.validate_on_submit():
            # se sim verifica se a data informada no formulário já foi agendada
            if form_solicitacao.data.data in datas_agendadas:
                # se sim retorna a mensagem
                flash('Data já agendada, escolha outra!', 'warning')
            else:
                # se ainda não foi agendada cria uma nova solicitação com base nos dados exigidos pelo banco de dados
                solicitacao = Solicitacao(
                    servico=form_solicitacao.servico.data,
                    motivo=form_solicitacao.motivo.data,
                    data=form_solicitacao.data.data,
                    usuario_id=current_user.id,
                    user_name=current_user.username
                )
                # adiciona a solicitação ao banco de dados
                database.session.add(solicitacao)
                # salva no banco de dados
                database.session.commit()
                # retorna a mensagem de sucesso
                flash('Solicitação enviada com sucesso!', 'success')
                # redireciona para a homepage
            return redirect(url_for('homepage'))
        # verifica os dados informados no formulário de consulta são válidos
        if form_consulta.validate_on_submit():
            # se sim, cria uma nova consulta
            consulta = Consulta(
                usuario_id=form_consulta.username.data,
                servico=form_consulta.servico.data,
                data=form_consulta.data.data,
                user_name=Usuario.query.get(form_consulta.username.data).username
            )
            # adiciona no banco de dados
            database.session.add(consulta)
            # salva no banco de dados, retorna a mensagem de sucesso e redireciona
            database.session.commit()
            flash('Consulta agendada com sucesso!', 'success')
            return redirect(url_for('homepage'))
        # retorna o template html da consulta, is_admin para verificar se o usuário é ou não um ADM, users que armazena todos os usuários, form_solicitacao a instancia do formuário de solicitação, form_consulta a instancia do formulário de consulta, as datas que já foram agendadas, solicitacoesPorUsuario as solicitações de cadas usuário, solicitacoes todas as solicitações, consultasPorUsuario as consultas de cada usuário e todas as consultas
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

# rota para cancelar consulta atravéz do id e permite publicar dados no banco de dados
@app.route('/cancelarConsulta/<int:id>', methods=['POST'])
# função para cancelar uma consulta, exige um id para funcionar
def cancelarConsulta(id):
    # pega o id da solicitação caso ele exista
    consulta = Consulta.query.get_or_404(id)
    # deleta a consulta
    database.session.delete(consulta)
    # salva o banco de dados, retorna a mensagem de sucesso e redireciona
    database.session.commit()
    flash('Consulta cancelada.', 'info')
    return redirect(url_for('homepage'))

# rota para cancelar solicitação atravéz do id e permite publicar dados no banco de dados
@app.route('/cancelarSolicitacao/<int:id>', methods=['POST'])
# função para cancelar uma solicitação, exige um id para funcionar
def cancelarSolicitacao(id):
    # pega o id da solicitação caso ele exista
    solicitacao = Solicitacao.query.get_or_404(id)
    # deleta a solicitação
    database.session.delete(solicitacao)
    # salva o banco de dados, retorna a mensagem de sucesso e redireciona
    database.session.commit()
    flash('Consulta cancelada.', 'info')
    return redirect(url_for('homepage'))

# rota para confirmar consulta atravéz do id e permite publicar dados no banco de dados
@app.route('/confirmar/<int:id>', methods=['POST'])
# função para cancelar uma consulta, exige um id para funcionar
def confirmar(id):
    # pega o id da solicitação caso ele exista
    solicitacao = Solicitacao.query.get_or_404(id)
    # cria uma nova consulta com base nos dados exigidos no banco de dados
    consulta = Consulta(
        servico=solicitacao.servico,
        motivo=solicitacao.motivo,
        data=solicitacao.data,
        user_name=solicitacao.user_name,
        usuario_id=solicitacao.usuario_id,
    )
    # adiciona a consulta
    database.session.add(consulta)
    # deleta a solicitação daquela consulta
    database.session.delete(solicitacao)
    # salva o banco de dados, retorna a mensagem de sucesso e redireciona
    database.session.commit()
    flash('Solicitação confirmada!', 'success')
    return redirect(url_for('homepage'))


# rota para cancelar uma consulta, <int:id> diz o id da consulta
@app.route('/cancelar/<int:id>', methods=['POST'])
# função para cancelar uma consulta, exige um id para funcionar
def cancelar(id):
    # pega o id da consula caso ele exista
    solicitacao = Solicitacao.query.get_or_404(id)
    # deleta a consulta selecionada
    database.session.delete(solicitacao)
    # salva o banco de dados e retorna a mensagem, depois redireciona para a homepage
    database.session.commit()
    flash('Solicitação cancelada.', 'info')
    return redirect(url_for('homepage'))


# Rota para promover um usuário a administrador (acessível apenas por outros administradores)
@app.route('/promote', methods=['POST'])
# apenas ADMs logados podem usar essa função
@login_required
def promote():
    # se o usuário atual não for um ADM, recebe a mensagem de acesso negado e é redirecionado para a homepage
    if not current_user.is_admin:
        flash('Acesso negado.')
        return redirect(url_for('homepage'))

    # Pega o ID do usuário
    user_id = request.form.get('user_id') 
    # pega o campo que define s eum usuário é um administrador 
    user = Usuario.query.get(user_id)
    if user:
        # armazena o valor True no campo is_admin, tornando o usuário selecionaod em um ADM
        user.is_admin = True  # Promove o usuário a administrador
        # salva o banco de dados e retorna a mensagem 
        database.session.commit()
        flash(f'O usuário {user.username} foi promovido a administrador.')
    else:
        flash('Usuário não encontrado.')
    return redirect(url_for('homepage'))


