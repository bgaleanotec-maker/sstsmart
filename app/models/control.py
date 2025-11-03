# app/models/control.py Modelo para Controles SST Decreto 1072/2015 - Resolución 0312/2019


from app import db
from datetime import datetime
from enum import Enum

class TipoControl(Enum):
    """Tipos de control según estándares"""
    PREVENTIVO = "Preventivo"
    CORRECTIVO = "Correctivo"
    DETECTIVO = "Detectivo"
    MITIGANTE = "Mitigante"

class NivelControl(Enum):
    """Niveles de control - Jerarquía de controles"""
    FUENTE = "En la Fuente"
    MEDIO = "En el Medio"
    INDIVIDUO = "En el Individuo"
    ADMINISTRATIVO = "Administrativo"

class EstadoControl(Enum):
    """Estados del control en su ciclo de vida"""
    PLANIFICADO = "Planificado"
    EN_PROCESO = "En Proceso"
    IMPLEMENTADO = "Implementado"
    VERIFICADO = "Verificado"
    EFECTIVO = "Efectivo"
    INEFECTIVO = "Inefectivo"
    CANCELADO = "Cancelado"

class Control(db.Model):
    """
    Control para mitigar riesgos
    Un control puede mitigar múltiples riesgos
    Un riesgo puede tener múltiples controles
    """
    __tablename__ = 'controles'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Identificación
    codigo = db.Column(db.String(50), unique=True, nullable=False)  # Ej: CTL-001-2025
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    
    # Clasificación
    tipo_control = db.Column(db.String(50), default=TipoControl.PREVENTIVO.value)  # Preventivo, Correctivo, Detectivo, Mitigante
    nivel_control = db.Column(db.String(50), default=NivelControl.FUENTE.value)  # Fuente, Medio, Individuo, Administrativo
    
    # Relaciones
    riesgo_id = db.Column(db.Integer, db.ForeignKey('riesgos_matriz.id'), nullable=False)
    responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Fechas
    fecha_planeada = db.Column(db.DateTime)
    fecha_implementacion = db.Column(db.DateTime)
    fecha_verificacion = db.Column(db.DateTime)
    fecha_cierre = db.Column(db.DateTime)
    
    # Estado
    estado = db.Column(db.String(50), default=EstadoControl.PLANIFICADO.value)
    
    # Efectividad
    efectividad_porcentaje = db.Column(db.Integer, default=0)  # 0-100%
    evidencia_implementacion = db.Column(db.Text)  # URLs a archivos, descripciones
    
    # Auditoría
    presupuesto_estimado = db.Column(db.Float)
    presupuesto_real = db.Column(db.Float)
    
    # Seguimiento
    requiere_seguimiento_periodico = db.Column(db.Boolean, default=False)
    frecuencia_seguimiento_dias = db.Column(db.Integer)  # Cada X días
    ultima_revision = db.Column(db.DateTime)
    
    # Sistema
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    riesgo = db.relationship('RiesgoMatriz', backref='controles')
    responsable = db.relationship('Usuario', backref='controles_asignados')
    acciones_seguimiento = db.relationship('SeguimientoControl', backref='control', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Control {self.codigo} - {self.nombre}>'
    
    def marcar_implementado(self, evidencia=""):
        """Marca el control como implementado"""
        self.estado = EstadoControl.IMPLEMENTADO.value
        self.fecha_implementacion = datetime.utcnow()
        self.evidencia_implementacion = evidencia
        
    def marcar_verificado(self, efectividad=100):
        """Marca el control como verificado"""
        self.estado = EstadoControl.VERIFICADO.value
        self.fecha_verificacion = datetime.utcnow()
        self.efectividad_porcentaje = efectividad
        
        if efectividad >= 80:
            self.estado = EstadoControl.EFECTIVO.value
        else:
            self.estado = EstadoControl.INEFECTIVO.value
    
    def cerrar(self):
        """Cierra el control"""
        self.estado = EstadoControl.EFECTIVO.value if self.efectividad_porcentaje >= 80 else EstadoControl.INEFECTIVO.value
        self.fecha_cierre = datetime.utcnow()


class SeguimientoControl(db.Model):
    """
    Seguimiento periódico de controles implementados
    Para verificar que se mantienen efectivos
    """
    __tablename__ = 'seguimientos_control'
    
    id = db.Column(db.Integer, primary_key=True)
    
    control_id = db.Column(db.Integer, db.ForeignKey('controles.id'), nullable=False)
    
    # Información
    fecha_revision = db.Column(db.DateTime, default=datetime.utcnow)
    responsable_revision_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Evaluación
    sigue_vigente = db.Column(db.Boolean, default=True)
    efectividad_actual = db.Column(db.Integer)  # 0-100%
    observaciones = db.Column(db.Text)
    
    # Acciones correctivas si es necesario
    requiere_ajustes = db.Column(db.Boolean, default=False)
    ajustes_recomendados = db.Column(db.Text)
    
    # Sistema
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    responsable_revision = db.relationship('Usuario')
    
    def __repr__(self):
        return f'<SeguimientoControl {self.control_id} - {self.fecha_revision.date()}>'