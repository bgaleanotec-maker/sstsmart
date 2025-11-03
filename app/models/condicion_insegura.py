from app import db
from datetime import datetime
import uuid

class CondicionInsegura(db.Model):
    __tablename__ = 'condiciones_inseguras'
    id = db.Column(db.Integer, primary_key=True)
    numero_reporte = db.Column(db.String(50), unique=True, nullable=False, index=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    ubicacion = db.Column(db.String(200))
    imagen_url = db.Column(db.String(300))
    imagen_procesada_json = db.Column(db.JSON)
    riesgos_identificados = db.Column(db.JSON)
    severidad_calculada = db.Column(db.Integer)
    empleado_reportador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    responsable_sst_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    estado = db.Column(db.String(30), default='Abierto')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    fecha_cierre = db.Column(db.DateTime)
    observaciones_ia = db.Column(db.Text)
    autorizado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_autorizacion = db.Column(db.DateTime)
    cumple_norma = db.Column(db.Boolean, default=False)
    metadata_adicional = db.Column(db.JSON)
    
    reportador = db.relationship('Usuario', foreign_keys=[empleado_reportador_id])
    responsable_sst = db.relationship('Usuario', foreign_keys=[responsable_sst_id])
    autorizador = db.relationship('Usuario', foreign_keys=[autorizado_por_id])
    
    def generar_numero_reporte(self):
        año = datetime.utcnow().year
        numero = str(uuid.uuid4().int)[:6]
        self.numero_reporte = f"REP-{año}-{numero}"
    
    def __repr__(self):
        return f'<CondicionInsegura {self.numero_reporte}>'
