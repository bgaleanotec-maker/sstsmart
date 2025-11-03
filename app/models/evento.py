from app import db
from datetime import datetime

class Evento(db.Model):
    __tablename__ = 'eventos'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    condicion_insegura_id = db.Column(db.Integer, db.ForeignKey('condiciones_inseguras.id'))
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    estado = db.Column(db.String(30), default='Abierto')
    prioridad = db.Column(db.Integer)
    responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_prevista_apertura = db.Column(db.DateTime)
    fecha_apertura_real = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_prevista_cierre = db.Column(db.DateTime)
    fecha_cierre_real = db.Column(db.DateTime)
    persona_afectada_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    numero_persona_afectada = db.Column(db.Integer)
    dias_incapacidad = db.Column(db.Integer, default=0)
    costo_estimado = db.Column(db.Float)
    investigacion_realizada = db.Column(db.Boolean, default=False)
    efectividad_accion = db.Column(db.Integer)
    auditor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_auditoria = db.Column(db.DateTime)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    responsable = db.relationship('Usuario', foreign_keys=[responsable_id])
    persona_afectada = db.relationship('Usuario', foreign_keys=[persona_afectada_id])
    auditor = db.relationship('Usuario', foreign_keys=[auditor_id])
    condicion_insegura = db.relationship('CondicionInsegura')
    
    def __repr__(self):
        return f'<Evento {self.titulo}>'
