# app/models/riesgo.py - REEMPLAZA TODO CON ESTO:

from app import db
from datetime import datetime

class RiesgoMatriz(db.Model):
    __tablename__ = 'riesgo_matriz'
    id = db.Column(db.Integer, primary_key=True)
    nombre_riesgo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    probabilidad = db.Column(db.Integer)
    severidad = db.Column(db.Integer)
    clasificacion = db.Column(db.Integer)
    empresa_id = db.Column(db.Integer)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    # La relación apunta a Control desde control.py
    controles = db.relationship('Control', back_populates='riesgo', lazy='dynamic')
    
    def calcular_clasificacion(self):
        self.clasificacion = self.probabilidad * self.severidad
        return self.clasificacion
    
    def nivel_riesgo(self):
        n = self.clasificacion
        if n <= 2: return "ACEPTABLE"
        elif n <= 4: return "TOLERABLE"
        elif n <= 9: return "MODERADO"
        else: return "INACEPTABLE"
    
    def __repr__(self):
        return f'<RiesgoMatriz {self.nombre_riesgo}>'

