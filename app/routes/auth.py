import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import or_
from flask_login import login_user, logout_user, current_user
from app.models import Usuarios
from app import db
from app.utils import custom_encrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar-senha')
        
        # Verifica se todos os campos foram preenchidos
        if not nome or not email or not senha or not confirmar_senha:
            error_message = "Preencha todos os campos."
            return render_template('cadastro.html', error_message=error_message)
        
        # Validação: Nome de usuário deve ter no mínimo 5 caracteres
        if len(nome) < 5:
            error_message = "O nome de usuário deve ter no mínimo 5 caracteres."
            return render_template('cadastro.html', error_message=error_message)
        
        # Verifica se as senhas conferem
        if senha != confirmar_senha:
            error_message = "As senhas não conferem."
            return render_template('cadastro.html', error_message=error_message)
        
        # Validação: Senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula e um número
        if len(senha) < 8:
            error_message = "A senha deve conter pelo menos 8 caracteres, incluindo uma letra maiúscula e um número."
            return render_template('cadastro.html', error_message=error_message)
        if not re.search(r'[A-Z]', senha) or not re.search(r'[0-9]', senha):
            error_message = "A senha deve conter pelo menos 8 caracteres, incluindo uma letra maiúscula e um número."
            return render_template('cadastro.html', error_message=error_message)
        
        # Verifica se o usuário já existe
        existing_user = Usuarios.query.filter(or_(Usuarios.username == nome, Usuarios.email == email)).first()
        if existing_user:
            error_message = "Usuário ou e-mail já cadastrado."
            return render_template('cadastro.html', error_message=error_message)
        
        encrypted_password = custom_encrypt(senha)
        new_user = Usuarios(username=nome, email=email, password_hash=encrypted_password)
        db.session.add(new_user)
        db.session.commit()
        
        success_message = "Cadastro realizado com sucesso!"
        return render_template('cadastro.html', success_message=success_message)
    else:
        return render_template('cadastro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = Usuarios.query.filter_by(email=email).first()
        if user is None or user.password_hash != custom_encrypt(senha):
            error_message = "Email ou senha incorretos."
            return render_template('login.html', error_message=error_message)
        login_user(user)
        return redirect(url_for('dashboard.dashboard'))
    else:
        return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.home'))
