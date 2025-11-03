from app import db
from datetime import datetime

class ConsultaJuridica(db.Model):
    __tablename__ = 'consultas_juridicas'
    id = db.Column(db.Integer, primary_key=True)
    numero_consulta = db.Column(db.String(50), unique=True, nullable=False, index=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    tipo_consulta = db.Column(db.String(50))  # Laboral, Penal, Civil, Administrativo
    condicion_insegura_id = db.Column(db.Integer, db.ForeignKey('condiciones_inseguras.id'))
    empleado_afectado_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    abogado_asignado_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    responsable_creador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    
    estado = db.Column(db.String(30), default='Abierta')  # Abierta, En revisión, Resuelta, Cerrada
    prioridad = db.Column(db.String(20), default='Normal')  # Baja, Normal, Alta, Crítica
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    fecha_asignacion = db.Column(db.DateTime)
    fecha_resolucion = db.Column(db.DateTime)
    fecha_cierre = db.Column(db.DateTime)
    
    resolucion = db.Column(db.Text)
    recomendaciones = db.Column(db.Text)
    normativa_aplicable = db.Column(db.JSON)
    riesgo_legal = db.Column(db.String(50))  # Bajo, Medio, Alto, Crítico
    notificacion_enviada = db.Column(db.Boolean, default=False)
    
    condicion_insegura = db.relationship('CondicionInsegura')
    empleado_afectado = db.relationship('Usuario', foreign_keys=[empleado_afectado_id])
    abogado = db.relationship('Usuario', foreign_keys=[abogado_asignado_id])
    responsable_creador = db.relationship('Usuario', foreign_keys=[responsable_creador_id])
    documentos = db.relationship('DocumentoLegal', backref='consulta', lazy='dynamic', cascade='all, delete-orphan')
    
    def generar_numero_consulta(self):
        import uuid
        año = datetime.utcnow().year
        numero = str(uuid.uuid4().int)[:6]
        self.numero_consulta = f"CONS-JUR-{año}-{numero}"
    
    def __repr__(self):
        return f'<ConsultaJuridica {self.numero_consulta}>'

class DocumentoLegal(db.Model):
    __tablename__ = 'documentos_legales'
    id = db.Column(db.Integer, primary_key=True)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consultas_juridicas.id'), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50))  # Contrato, Dictamen, Constancia, etc.
    ruta_archivo = db.Column(db.String(300))
    contenido = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    creado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    
    creado_por = db.relationship('Usuario')
    
    def __repr__(self):
        return f'<DocumentoLegal {self.nombre}>'
