from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import create_access_token
from app import db
from app.models import Usuario
from app.routes import auth_bp
from datetime import datetime

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(password):
            if not usuario.activo:
                flash('Usuario inactivo', 'error')
                return redirect(url_for('auth.login'))
            
            login_user(usuario)
            usuario.ultimo_login = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('dashboard.index'))
        flash('Email o contraseña incorrectos', 'error')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/api/token', methods=['POST'])
def get_token():
    email = request.json.get('email')
    password = request.json.get('password')
    usuario = Usuario.query.filter_by(email=email).first()
    
    if usuario and usuario.check_password(password):
        access_token = create_access_token(identity=usuario.id)
        return {'access_token': access_token}, 200
    return {'error': 'Credenciales inválidas'}, 401
