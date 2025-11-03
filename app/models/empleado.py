from app import db
from datetime import datetime

class Empleado(db.Model):
    __tablename__ = 'empleados'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, unique=True)
    tipo = db.Column(db.String(20), default='Empleado')
    cargo = db.Column(db.String(100))
    departamento = db.Column(db.String(100))
    centro_de_costo = db.Column(db.String(50))
    riesgo_asignado = db.Column(db.String(50))
    datos_contacto = db.Column(db.String(120))
    atributos_especiales = db.Column(db.JSON, default={})
    fecha_ingreso = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    usuario = db.relationship('Usuario', backref='empleado')
    
    def __repr__(self):
        return f'<Empleado {self.usuario.nombre_completo}>'
