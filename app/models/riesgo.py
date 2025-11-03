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
    
    controles = db.relationship('Control', backref='riesgo', lazy='dynamic')
    
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

class Control(db.Model):
    __tablename__ = 'controles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    tipo = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(50), default='Activo')
    riesgo_id = db.Column(db.Integer, db.ForeignKey('riesgo_matriz.id'))
    responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_implementacion = db.Column(db.DateTime)
    efectividad = db.Column(db.Integer, default=0)
    norma_aplicable = db.Column(db.String(100))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    responsable = db.relationship('Usuario')
    
    def __repr__(self):
        return f'<Control {self.nombre}>'
