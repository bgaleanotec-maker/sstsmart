from app import db
from datetime import datetime

class ConfiguracionIA(db.Model):
    __tablename__ = 'configuracion_ia'
    id = db.Column(db.Integer, primary_key=True)
    nombre_modelo = db.Column(db.String(100), default='Gemini-1.5-pro-vision')
    proveedor = db.Column(db.String(50), default='Google')
    api_key_encrypted = db.Column(db.String(500))
    prompt_sistema = db.Column(db.Text)
    comportamientos_entrena = db.Column(db.JSON)
    umbral_confianza = db.Column(db.Float, default=0.75)
    tipos_riesgos_detecta = db.Column(db.JSON)
    base_conocimientos = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = db.Column(db.Integer, default=1)
    
    def __repr__(self):
        return f'<ConfiguracionIA {self.nombre_modelo}>'
