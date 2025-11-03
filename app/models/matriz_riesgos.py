from app import db
from datetime import datetime, timedelta
from enum import Enum

class NivelSeveridad(Enum):
    """Niveles de severidad según matriz ICONTEC"""
    MINIMO = 1
    BAJO = 2
    MEDIO = 3
    ALTO = 4
    CRITICO = 5

class NivelProbabilidad(Enum):
    """Niveles de probabilidad"""
    REMOTA = 1
    BAJA = 2
    MEDIA = 3
    ALTA = 4
    MUY_ALTA = 5

class NivelRiesgo(db.Model):
    """
    Define los niveles de riesgo resultantes de la matriz
    Ejemplo: Verde (Aceptable), Amarillo (Tolerable), Naranja (Moderado), Rojo (Inaceptable)
    """
    __tablename__ = 'niveles_riesgo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)  # Aceptable, Tolerable, Moderado, Inaceptable
    descripcion = db.Column(db.Text)
    color = db.Column(db.String(7), default='#00FF00')  # Color hex
    rango_minimo = db.Column(db.Integer)  # Ej: 1
    rango_maximo = db.Column(db.Integer)  # Ej: 4
    requiere_accion = db.Column(db.Boolean, default=False)  # ¿Requiere acción correctiva?
    activo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<NivelRiesgo {self.nombre}>'

class ReglasEscalonamiento(db.Model):
    """
    Define las reglas de escalamiento automático
    Ejemplo: Si no se gestiona en 30 min → escalona a supervisor, luego a gerente
    """
    __tablename__ = 'reglas_escalonamiento'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    
    # Condiciones
    nivel_riesgo_minimo = db.Column(db.Integer)  # Aplica a qué rango de riesgo
    nivel_riesgo_maximo = db.Column(db.Integer)
    
    # Tiempos en minutos
    tiempo_respuesta_minutos = db.Column(db.Integer)  # Ej: 30 minutos
    tiempo_resolucion_minutos = db.Column(db.Integer)  # Ej: 1440 minutos = 1 día
    
    # Escalamiento
    escalamientos = db.relationship('PasoEscalonamiento', backref='regla', lazy='dynamic', cascade='all, delete-orphan')
    
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ReglasEscalonamiento {self.nombre}>'

class PasoEscalonamiento(db.Model):
    """
    Pasos secuenciales en el escalamiento
    Paso 1: Asignar a gestor de RRHH (5 min después)
    Paso 2: Si no responde, asignar a Gerente (30 min después)
    Paso 3: Si no responde, asignar a Dirección (60 min después)
    """
    __tablename__ = 'pasos_escalonamiento'
    id = db.Column(db.Integer, primary_key=True)
    regla_id = db.Column(db.Integer, db.ForeignKey('reglas_escalonamiento.id'), nullable=False)
    
    numero_paso = db.Column(db.Integer)  # Paso 1, 2, 3...
    descripcion = db.Column(db.String(200))
    
    # A quién escalona
    rol_destino = db.Column(db.String(50))  # Ej: "Gestor_RRHH", "Gerente", "Dirección"
    
    # Tiempo después del paso anterior
    minutos_delay = db.Column(db.Integer)  # Ej: 5, 30, 60
    
    # Acciones al escalionar
    enviar_notificacion = db.Column(db.Boolean, default=True)
    crear_tarea = db.Column(db.Boolean, default=True)
    
    activo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<PasoEscalonamiento Paso {self.numero_paso}>'

class MatrizRiesgos(db.Model):
    """
    Matriz de riesgos: Probabilidad x Severidad = Nivel de Riesgo
    Cada celda define qué gestor debe atenderlo y en cuánto tiempo
    """
    __tablename__ = 'matriz_riesgos'
    id = db.Column(db.Integer, primary_key=True)
    
    # Coordenadas
    probabilidad = db.Column(db.Integer)  # 1-5
    severidad = db.Column(db.Integer)  # 1-5
    
    # Resultado
    nivel_riesgo_id = db.Column(db.Integer, db.ForeignKey('niveles_riesgo.id'))
    valor_riesgo = db.Column(db.Integer)  # Probabilidad * Severidad
    
    # Gestión
    regla_escalonamiento_id = db.Column(db.Integer, db.ForeignKey('reglas_escalonamiento.id'))
    
    activa = db.Column(db.Boolean, default=True)
    
    nivel_riesgo_obj = db.relationship('NivelRiesgo')
    regla_escalonamiento_obj = db.relationship('ReglasEscalonamiento')
    
    def __repr__(self):
        return f'<MatrizRiesgos {self.probabilidad}x{self.severidad}>'

class GestorResponsabilidades(db.Model):
    """
    Define quién es responsable de qué tipo de incidente
    Ej: Incidente CRITICO → Gestor_RRHH (principal), Abogado (backup)
    """
    __tablename__ = 'gestor_responsabilidades'
    id = db.Column(db.Integer, primary_key=True)
    
    # Qué condición dispara esto
    nivel_riesgo_id = db.Column(db.Integer, db.ForeignKey('niveles_riesgo.id'))
    tipo_reporte_id = db.Column(db.Integer, db.ForeignKey('tipos_reportes.id'))
    
    # Gestores responsables (en orden de jerarquía)
    rol_principal = db.Column(db.String(50), nullable=False)  # Ej: "Gestor_RRHH"
    rol_backup_1 = db.Column(db.String(50))  # Ej: "Gerente"
    rol_backup_2 = db.Column(db.String(50))  # Ej: "Dirección"
    
    # Departamentos específicos si aplica
    departamento = db.Column(db.String(100))  # Ej: "Producción", "Logística"
    
    # Notificaciones adicionales
    notificar_roles = db.Column(db.JSON)  # Ej: ["Abogado", "Médico_Ocupacional"]
    
    # Configuración de tiempo
    tiempo_respuesta_minutos = db.Column(db.Integer, default=30)
    tiempo_resolucion_minutos = db.Column(db.Integer, default=1440)  # 1 día
    
    activo = db.Column(db.Boolean, default=True)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    nivel_riesgo_obj = db.relationship('NivelRiesgo')
    tipo_reporte_obj = db.relationship('TipoReporte')
    
    def __repr__(self):
        return f'<GestorResponsabilidades {self.rol_principal}>'

class GestionReporte(db.Model):
    """
    Tracking de la gestión de cada reporte
    Quién lo tiene, en qué paso está, cuándo fue asignado, cuándo debe resolverse
    """
    __tablename__ = 'gestion_reportes'
    id = db.Column(db.Integer, primary_key=True)
    
    # Reporte
    reporte_id = db.Column(db.Integer, db.ForeignKey('condiciones_inseguras.id'), nullable=False)
    
    # Gestión actual
    gestor_actual_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    rol_gestor = db.Column(db.String(50))  # Ej: "Gestor_RRHH"
    
    # Responsabilidad configurada
    gestor_responsabilidad_id = db.Column(db.Integer, db.ForeignKey('gestor_responsabilidades.id'))
    
    # Estados del flujo
    estado = db.Column(db.String(30), default='Asignado')  # Asignado, En_Proceso, En_Espera, Escalado, Resuelto, Cerrado
    
    # Tiempos
    fecha_asignacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_vencimiento_respuesta = db.Column(db.DateTime)  # Cuándo debe responder
    fecha_vencimiento_resolucion = db.Column(db.DateTime)  # Cuándo debe resolver
    fecha_respuesta = db.Column(db.DateTime)  # Cuándo respondió realmente
    fecha_resolucion = db.Column(db.DateTime)  # Cuándo resolvió realmente
    
    # Escalamiento
    numero_escalamiento = db.Column(db.Integer, default=0)
    fecha_proximo_escalamiento = db.Column(db.DateTime)
    escalado_a_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))  # Gestor escalado
    
    # Historial
    historial_cambios = db.Column(db.JSON)  # Array de {fecha, usuario, accion, descripcion}
    
    # Notas
    notas_internas = db.Column(db.Text)
    
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    reporte = db.relationship('CondicionInsegura', backref='gestiones')
    gestor_actual = db.relationship('Usuario', foreign_keys=[gestor_actual_id])
    gestor_escalado = db.relationship('Usuario', foreign_keys=[escalado_a_id])
    gestor_responsabilidad = db.relationship('GestorResponsabilidades')
    
    def __repr__(self):
        return f'<GestionReporte {self.reporte_id} - {self.estado}>'
    
    def calcular_vencimientos(self, tiempo_respuesta_min, tiempo_resolucion_min):
        """Calcula fechas de vencimiento basado en minutos"""
        self.fecha_vencimiento_respuesta = datetime.utcnow() + timedelta(minutes=tiempo_respuesta_min)
        self.fecha_vencimiento_resolucion = datetime.utcnow() + timedelta(minutes=tiempo_resolucion_min)
    
    def esta_vencido_respuesta(self):
        """¿Se venció el tiempo de respuesta?"""
        if not self.fecha_respuesta and self.fecha_vencimiento_respuesta:
            return datetime.utcnow() > self.fecha_vencimiento_respuesta
        return False
    
    def esta_vencido_resolucion(self):
        """¿Se venció el tiempo de resolución?"""
        if not self.fecha_resolucion and self.fecha_vencimiento_resolucion:
            return datetime.utcnow() > self.fecha_vencimiento_resolucion
        return False
    
    def agregar_cambio(self, usuario_id, accion, descripcion):
        """Agrega un evento al historial"""
        if not self.historial_cambios:
            self.historial_cambios = []
        
        self.historial_cambios.append({
            'fecha': datetime.utcnow().isoformat(),
            'usuario_id': usuario_id,
            'accion': accion,
            'descripcion': descripcion
        })

class TareaGestion(db.Model):
    """
    Tareas generadas automáticamente para gestores
    Se crean cuando se asigna un reporte
    """
    __tablename__ = 'tareas_gestion'
    id = db.Column(db.Integer, primary_key=True)
    
    gestion_reporte_id = db.Column(db.Integer, db.ForeignKey('gestion_reportes.id'), nullable=False)
    asignado_a_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    titulo = db.Column(db.String(200))
    descripcion = db.Column(db.Text)
    
    # Estados
    estado = db.Column(db.String(30), default='Abierta')  # Abierta, En_Progreso, Completada, Delegada, Cancelada
    
    # Prioridad basada en riesgo
    prioridad = db.Column(db.Integer)  # 1 (baja) a 5 (crítica)
    
    # Fechas
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_vencimiento = db.Column(db.DateTime)
    fecha_completada = db.Column(db.DateTime)
    
    # Relaciones
    gestion_reporte = db.relationship('GestionReporte')
    asignado_a = db.relationship('Usuario')
    
    def __repr__(self):
        return f'<TareaGestion {self.titulo}>'