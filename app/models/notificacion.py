from app import db
from datetime import datetime

class Notificacion(db.Model):
    __tablename__ = 'notificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(20), default='info') # info, success, warning, error
    leida = db.Column(db.Boolean, default=False)
    link = db.Column(db.String(255)) # URL opcional para redirigir
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    usuario = db.relationship('Usuario', backref=db.backref('notificaciones', lazy='dynamic'))

    def __repr__(self):
        return f'<Notificacion {self.id} User:{self.usuario_id}>'
