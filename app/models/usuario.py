from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    contraseña_hash = db.Column(db.String(255), nullable=False)
    nombre_completo = db.Column(db.String(120), nullable=False)
    rol = db.Column(db.String(30), default='Empleado', nullable=False)
    activo = db.Column(db.Boolean, default=True)
    ultimo_login = db.Column(db.DateTime)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.contraseña_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.contraseña_hash, password)
    
    def tiene_rol(self, *roles):
        return self.rol in roles
    
    def __repr__(self):
        return f'<Usuario {self.email}>'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
