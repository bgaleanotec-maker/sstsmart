# app/models/control.py
"""
Modelo para Controles SST
Decreto 1072/2015 - Resolución 0312/2019
"""

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
    ASIGNADO = "Asignado"
    EN_PROCESO = "En Proceso"
    IMPLEMENTADO = "Implementado"
    VERIFICADO = "Verificado"
    EFECTIVO = "Efectivo"
    INEFECTIVO = "Inefectivo"
    REQUIERE_AJUSTE = "Requiere Ajuste"
    CERRADO = "Cerrado"
    CANCELADO = "Cancelado"


class Control(db.Model):
    """
    Control para mitigar riesgos
    Un control puede mitigar múltiples riesgos
    Un riesgo puede tener múltiples controles
    
    Ciclo de vida:
    1. PLANIFICADO → Se define el control
    2. ASIGNADO → Se asigna responsable
    3. EN_PROCESO → Se está implementando
    4. IMPLEMENTADO → Se ejecutó
    5. VERIFICADO → Se verificó la implementación
    6. EFECTIVO/INEFECTIVO → Según efectividad
    7. REQUIERE_AJUSTE → Necesita mejoras
    8. CERRADO → Finalizado
    9. CANCELADO → No aplica
    """
    __tablename__ = 'controles'
    
    # ========== IDENTIFICACIÓN ==========
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False, index=True)  # Ej: CTL-001-2025
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    
    # ========== CLASIFICACIÓN ==========
    tipo_control = db.Column(
        db.String(50),
        default=TipoControl.PREVENTIVO.value,
        nullable=False
    )  # Preventivo, Correctivo, Detectivo, Mitigante
    
    nivel_control = db.Column(
        db.String(50),
        default=NivelControl.FUENTE.value,
        nullable=False
    )  # Fuente, Medio, Individuo, Administrativo
    
    # ========== RELACIONES ==========
    # Vínculo con riesgo
    riesgo_id = db.Column(
        db.Integer,
        db.ForeignKey('riesgo_matriz.id'),
        nullable=False,
        index=True
    )
    
    # Responsable de implementar el control
    responsable_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False,
        index=True
    )
    
    # Quién creó el control (auditoría)
    creado_por = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=True
    )
    
    # Rol del usuario que creó (auditoría)
    creado_por_rol = db.Column(db.String(100))
    
    # ========== FECHAS DE CICLO DE VIDA ==========
    fecha_planeada = db.Column(db.DateTime)  # Cuándo se planea implementar
    fecha_implementacion = db.Column(db.DateTime)  # Cuándo se implementó
    fecha_verificacion = db.Column(db.DateTime)  # Cuándo se verificó
    fecha_cierre = db.Column(db.DateTime)  # Cuándo se cerró
    
    # ========== ESTADO ==========
    estado = db.Column(
        db.String(50),
        default=EstadoControl.PLANIFICADO.value,
        nullable=False,
        index=True
    )
    
    # ========== EFECTIVIDAD ==========
    efectividad_porcentaje = db.Column(db.Integer, default=0)  # 0-100%
    evidencia_implementacion = db.Column(db.Text)  # URLs, descripciones, archivos adjuntos
    
    # ========== PRESUPUESTO ==========
    presupuesto_estimado = db.Column(db.Float)  # Costo planeado
    presupuesto_real = db.Column(db.Float)  # Costo ejecutado
    
    # ========== SEGUIMIENTO PERIÓDICO ==========
    requiere_seguimiento_periodico = db.Column(db.Boolean, default=False)
    frecuencia_seguimiento_dias = db.Column(db.Integer, default=30)  # Cada X días
    ultima_revision = db.Column(db.DateTime)  # Última vez que se revisó
    proximo_seguimiento = db.Column(db.DateTime)  # Cuándo es el próximo
    
    # ========== AUDITORÍA ==========
    activo = db.Column(db.Boolean, default=True, index=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    actualizado_en = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # ========== RELACIONES ORM ==========
    riesgo = db.relationship('RiesgoMatriz', back_populates='controles', foreign_keys=[riesgo_id])
    responsable = db.relationship(
        'Usuario',
        backref='controles_asignados',
        foreign_keys=[responsable_id]
    )
    usuario_creador = db.relationship(
        'Usuario',
        backref='controles_creados',
        foreign_keys=[creado_por]
    )
    acciones_seguimiento = db.relationship(
        'SeguimientoControl',
        backref='control',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        return f'<Control {self.codigo} - {self.nombre}>'
    
    # ========== MÉTODOS DE TRANSICIÓN DE ESTADO ==========
    
    def marcar_asignado(self):
        """Marca el control como asignado a responsable"""
        self.estado = EstadoControl.ASIGNADO.value
        self.actualizado_en = datetime.utcnow()
    
    def marcar_en_proceso(self):
        """Marca el control como en proceso de implementación"""
        self.estado = EstadoControl.EN_PROCESO.value
        self.actualizado_en = datetime.utcnow()
    
    def marcar_implementado(self, evidencia=""):
        """Marca el control como implementado"""
        self.estado = EstadoControl.IMPLEMENTADO.value
        self.fecha_implementacion = datetime.utcnow()
        self.evidencia_implementacion = evidencia
        self.actualizado_en = datetime.utcnow()
    
    def marcar_verificado(self, efectividad=100):
        """Marca el control como verificado y calcula efectividad"""
        self.estado = EstadoControl.VERIFICADO.value
        self.fecha_verificacion = datetime.utcnow()
        self.efectividad_porcentaje = efectividad
        self.actualizado_en = datetime.utcnow()
        
        # Transicionar a estado de efectividad
        if efectividad >= 80:
            self.estado = EstadoControl.EFECTIVO.value
        else:
            self.estado = EstadoControl.INEFECTIVO.value
    
    def marcar_requiere_ajuste(self):
        """Marca que el control requiere ajustes"""
        self.estado = EstadoControl.REQUIERE_AJUSTE.value
        self.actualizado_en = datetime.utcnow()
    
    def cerrar(self):
        """Cierra el control definiendo estado final"""
        self.estado = EstadoControl.CERRADO.value
        self.fecha_cierre = datetime.utcnow()
        self.activo = False
        self.actualizado_en = datetime.utcnow()
    
    def cancelar(self, razon=""):
        """Cancela el control"""
        self.estado = EstadoControl.CANCELADO.value
        self.fecha_cierre = datetime.utcnow()
        self.activo = False
        self.actualizado_en = datetime.utcnow()
    
    # ========== MÉTODOS DE LÓGICA DE NEGOCIO ==========
    
    def calcular_proximo_seguimiento(self):
        """Calcula la fecha del próximo seguimiento"""
        if self.requiere_seguimiento_periodico and self.frecuencia_seguimiento_dias:
            from datetime import timedelta
            ultima = self.ultima_revision or self.fecha_verificacion or datetime.utcnow()
            self.proximo_seguimiento = ultima + timedelta(days=self.frecuencia_seguimiento_dias)
            return self.proximo_seguimiento
        return None
    
    def es_debido_seguimiento(self):
        """Verifica si es debido hacer un seguimiento"""
        if not self.requiere_seguimiento_periodico:
            return False
        
        if not self.proximo_seguimiento:
            self.calcular_proximo_seguimiento()
        
        return self.proximo_seguimiento and self.proximo_seguimiento <= datetime.utcnow()
    
    def obtener_seguimientos_recientes(self, dias=30):
        """Obtiene seguimientos de los últimos X días"""
        from datetime import timedelta
        fecha_limite = datetime.utcnow() - timedelta(days=dias)
        return self.acciones_seguimiento.filter(
            SeguimientoControl.fecha_revision >= fecha_limite
        ).all()
    
    def obtener_efectividad_promedio(self):
        """Calcula la efectividad promedio de todos los seguimientos"""
        seguimientos = self.acciones_seguimiento.all()
        if not seguimientos:
            return self.efectividad_porcentaje or 0
        
        total = sum(s.efectividad_actual for s in seguimientos if s.efectividad_actual)
        return total / len(seguimientos) if seguimientos else 0
    
    def puede_cerrarse(self):
        """Verifica si el control puede cerrarse"""
        # No puede cerrarse si está en Planificado o Asignado
        estados_no_cerrables = [
            EstadoControl.PLANIFICADO.value,
            EstadoControl.ASIGNADO.value,
            EstadoControl.CANCELADO.value,
            EstadoControl.CERRADO.value
        ]
        return self.estado not in estados_no_cerrables
    
    def obtener_dias_sin_revisar(self):
        """Calcula cuántos días han pasado sin revisión"""
        fecha_revision = self.ultima_revision or self.fecha_verificacion or self.creado_en
        return (datetime.utcnow() - fecha_revision).days
    
    # ========== MÉTODOS DE VALIDACIÓN ==========
    
    def es_vigente(self):
        """Verifica si el control está vigente"""
        return self.activo and self.estado != EstadoControl.CANCELADO.value
    
    def esta_implementado(self):
        """Verifica si está implementado o verificado"""
        return self.estado in [
            EstadoControl.IMPLEMENTADO.value,
            EstadoControl.VERIFICADO.value,
            EstadoControl.EFECTIVO.value,
            EstadoControl.INEFECTIVO.value,
            EstadoControl.REQUIERE_AJUSTE.value
        ]
    
    def tiene_evidencia(self):
        """Verifica si tiene evidencia de implementación"""
        return bool(self.evidencia_implementacion)
    
    def to_dict(self):
        """Convierte el control a diccionario para API"""
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tipo_control': self.tipo_control,
            'nivel_control': self.nivel_control,
            'estado': self.estado,
            'efectividad': self.efectividad_porcentaje,
            'responsable': self.responsable.nombre if self.responsable else None,
            'riesgo': self.riesgo.nombre_riesgo if self.riesgo else None,
            'fecha_planeada': self.fecha_planeada.isoformat() if self.fecha_planeada else None,
            'fecha_implementacion': self.fecha_implementacion.isoformat() if self.fecha_implementacion else None,
            'fecha_verificacion': self.fecha_verificacion.isoformat() if self.fecha_verificacion else None
        }


class SeguimientoControl(db.Model):
    """
    Seguimiento periódico de controles implementados
    Para verificar que se mantienen efectivos
    
    Permite tracking de la efectividad del control a lo largo del tiempo
    """
    __tablename__ = 'seguimientos_control'
    
    # ========== IDENTIFICACIÓN ==========
    id = db.Column(db.Integer, primary_key=True)
    control_id = db.Column(
        db.Integer,
        db.ForeignKey('controles.id'),
        nullable=False,
        index=True
    )
    
    # ========== INFORMACIÓN DE REVISIÓN ==========
    fecha_revision = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    responsable_revision_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False
    )
    
    # ========== EVALUACIÓN ==========
    sigue_vigente = db.Column(db.Boolean, default=True)  # ¿Sigue siendo necesario?
    efectividad_actual = db.Column(db.Integer)  # 0-100% en esta revisión
    observaciones = db.Column(db.Text)  # Observaciones generales
    
    # ========== ACCIONES CORRECTIVAS ==========
    requiere_ajustes = db.Column(db.Boolean, default=False)
    ajustes_recomendados = db.Column(db.Text)  # Mejoras sugeridas
    
    # ========== AUDITORÍA ==========
    creado_en = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # ========== RELACIONES ORM ==========
    responsable_revision = db.relationship(
        'Usuario',
        foreign_keys=[responsable_revision_id]
    )
    
    def __repr__(self):
        return f'<SeguimientoControl {self.control_id} - {self.fecha_revision.date()}>'
    
    def to_dict(self):
        """Convierte el seguimiento a diccionario para API"""
        return {
            'id': self.id,
            'control_id': self.control_id,
            'fecha_revision': self.fecha_revision.isoformat(),
            'responsable': self.responsable_revision.nombre if self.responsable_revision else None,
            'sigue_vigente': self.sigue_vigente,
            'efectividad': self.efectividad_actual,
            'observaciones': self.observaciones,
            'requiere_ajustes': self.requiere_ajustes,
            'ajustes_recomendados': self.ajustes_recomendados
        }