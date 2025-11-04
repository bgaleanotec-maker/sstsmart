# app/models/juridico.py
"""
MÓDULO JURÍDICO - SST SMART
============================
Incluye:
- Pool de abogados con especialidades
- Consultas jurídicas con tracking completo
- Gestión documental con versionado
- Tabla de retención (Decreto 1072/2015, Art 2.2.3.1)
- Comentarios colaborativos
- Auditoría completa
"""

from app import db
from datetime import datetime, timedelta
import uuid
import json

# ==================== ABOGADOS ====================

class Abogado(db.Model):
    """Pool de abogados registrados en la plataforma"""
    __tablename__ = 'abogados'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True)
    
    # Información profesional
    numero_cedula = db.Column(db.String(20), unique=True, nullable=False)
    numero_tarjeta_profesional = db.Column(db.String(20), unique=True, nullable=False)
    especialidades = db.Column(db.JSON)  # ['Laboral', 'Penal', 'Civil', 'Administrativo']
    firma_digital = db.Column(db.String(500))  # Ruta del certificado
    
    # Disponibilidad y capacidad
    horas_disponibles = db.Column(db.Integer, default=20)  # Horas/semana
    tarifa_consulta_minuto = db.Column(db.Float)  # En COP
    estado_disponibilidad = db.Column(db.String(20), default='Disponible')  # Disponible, Ocupado, Vacaciones
    
    # Experiencia
    anos_experiencia = db.Column(db.Integer)
    casos_exitosos = db.Column(db.Integer, default=0)
    calificacion_promedio = db.Column(db.Float, default=5.0)
    
    # Contacto y localización
    telefono = db.Column(db.String(20))
    ciudad = db.Column(db.String(100))
    horario_atencion = db.Column(db.JSON)  # {'lunes': ['08:00', '17:00'], ...}
    
    # Auditoría
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    usuario = db.relationship('Usuario', backref='abogado_profile')
    consultas = db.relationship('ConsultaJuridica', backref='abogado', lazy='dynamic')
    calificaciones = db.relationship('CalificacionAbogado', backref='abogado', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Abogado {self.usuario.nombre_completo}>'
    
    def get_disponibilidad_hoy(self):
        """Retorna si está disponible hoy"""
        from datetime import datetime
        hoy = datetime.now().strftime('%A').lower()
        hoy_es = {'monday': 'lunes', 'tuesday': 'martes', 'wednesday': 'miercoles', 
                  'thursday': 'jueves', 'friday': 'viernes', 'saturday': 'sabado', 'sunday': 'domingo'}
        return hoy_es.get(datetime.now().strftime('%A').lower()) in self.horario_atencion


class CalificacionAbogado(db.Model):
    """Calificaciones de clientes a abogados"""
    __tablename__ = 'calificaciones_abogados'
    
    id = db.Column(db.Integer, primary_key=True)
    abogado_id = db.Column(db.Integer, db.ForeignKey('abogados.id'), nullable=False)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consultas_juridicas.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    puntuacion = db.Column(db.Integer)  # 1-5
    comentario = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)


# ==================== CONSULTAS JURÍDICAS ====================

class ConsultaJuridica(db.Model):
    """Consultas jurídicas con tracking completo"""
    __tablename__ = 'consultas_juridicas'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_consulta = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Información básica
    titulo = db.Column(db.String(300), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    tipo_consulta = db.Column(db.String(50), nullable=False)  # Laboral, Penal, Civil, Administrativo
    
    # Vinculaciones
    condicion_insegura_id = db.Column(db.Integer, db.ForeignKey('condiciones_inseguras.id'))
    empleado_afectado_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    abogado_asignado_id = db.Column(db.Integer, db.ForeignKey('abogados.id'))
    responsable_creador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Estados y seguimiento
    estado = db.Column(db.String(30), default='Abierta', index=True)
    # Abierta → En revisión → En concepto → Concepto emitido → Resuelta → Cerrada
    
    prioridad = db.Column(db.String(20), default='Normal')
    riesgo_legal = db.Column(db.String(50), default='Medio')
    
    # Confidencialidad (importante para documentos SST)
    nivel_confidencialidad = db.Column(db.String(20), default='Interno')  # Interno, Confidencial, Restringido
    
    # Fechas
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    fecha_asignacion = db.Column(db.DateTime)
    fecha_inicio_concepto = db.Column(db.DateTime)
    fecha_concepto_emitido = db.Column(db.DateTime)
    fecha_resolucion = db.Column(db.DateTime)
    fecha_cierre = db.Column(db.DateTime)
    
    # Horas de trabajo (para facturación)
    horas_estimadas = db.Column(db.Float)
    horas_reales = db.Column(db.Float, default=0.0)
    
    # Conceptos y recomendaciones
    concepto_legal = db.Column(db.Text)  # Concepto completo del abogado
    resolucion = db.Column(db.Text)
    recomendaciones = db.Column(db.Text)
    normativa_aplicable = db.Column(db.JSON)  # Decretos, resoluciones aplicables
    
    # Seguimiento
    proxima_accion = db.Column(db.String(500))
    proxima_fecha_seguimiento = db.Column(db.DateTime)
    
    # Auditoría
    notificacion_enviada = db.Column(db.Boolean, default=False)
    version = db.Column(db.Integer, default=1)  # Para cambios mayores
    
    # Relaciones
    condicion_insegura = db.relationship('CondicionInsegura')
    empleado_afectado = db.relationship('Usuario', foreign_keys=[empleado_afectado_id])
    responsable_creador = db.relationship('Usuario', foreign_keys=[responsable_creador_id])
    
    documentos = db.relationship('DocumentoLegal', backref='consulta', lazy='dynamic', 
                                cascade='all, delete-orphan')
    comentarios = db.relationship('ComentarioConsulta', backref='consulta', lazy='dynamic',
                                 cascade='all, delete-orphan')
    auditorias = db.relationship('AuditoriaConsulta', backref='consulta', lazy='dynamic',
                                cascade='all, delete-orphan')
    
    def generar_numero_consulta(self):
        """Genera número único de consulta"""
        año = datetime.utcnow().year
        mes = datetime.utcnow().month
        numero = str(uuid.uuid4().int)[:5]
        self.numero_consulta = f"JUR-{año}{mes:02d}-{numero}"
    
    def cambiar_estado(self, nuevo_estado, usuario_id, razon=''):
        """Cambia estado y registra auditoría"""
        estado_anterior = self.estado
        self.estado = nuevo_estado
        
        auditoria = AuditoriaConsulta(
            consulta_id=self.id,
            accion='cambio_estado',
            estado_anterior=estado_anterior,
            estado_nuevo=nuevo_estado,
            usuario_id=usuario_id,
            razon=razon
        )
        db.session.add(auditoria)
        
        # Actualizar fechas según estado
        if nuevo_estado == 'En revisión':
            self.fecha_asignacion = datetime.utcnow()
        elif nuevo_estado == 'En concepto':
            self.fecha_inicio_concepto = datetime.utcnow()
        elif nuevo_estado == 'Concepto emitido':
            self.fecha_concepto_emitido = datetime.utcnow()
        elif nuevo_estado == 'Resuelta':
            self.fecha_resolucion = datetime.utcnow()
        elif nuevo_estado == 'Cerrada':
            self.fecha_cierre = datetime.utcnow()
    
    def __repr__(self):
        return f'<ConsultaJuridica {self.numero_consulta}>'


# ==================== DOCUMENTOS CON VERSIONES ====================

class DocumentoLegal(db.Model):
    """Documentos asociados a consultas con control de versiones"""
    __tablename__ = 'documentos_legales'
    
    id = db.Column(db.Integer, primary_key=True)
    uid_documento = db.Column(db.String(50), unique=True, default=lambda: str(uuid.uuid4())[:12])
    
    # Metadatos
    consulta_id = db.Column(db.Integer, db.ForeignKey('consultas_juridicas.id'), nullable=False)
    nombre = db.Column(db.String(300), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Contrato, Dictamen, Concepto, Resolución, etc.
    descripcion = db.Column(db.Text)
    
    # Contenido y almacenamiento
    contenido = db.Column(db.Text)  # Para textos planos
    ruta_archivo = db.Column(db.String(500))  # Para PDFs, DOCX, etc.
    hash_documento = db.Column(db.String(64))  # SHA-256 para integridad
    tamano_bytes = db.Column(db.Integer)
    
    # Versionado
    numero_version = db.Column(db.Integer, default=1)
    documento_padre_id = db.Column(db.Integer, db.ForeignKey('documentos_legales.id'))
    es_version_anterior = db.Column(db.Boolean, default=False)
    
    # Metadatos legales
    clasificacion = db.Column(db.String(50))  # Confidencial, Interno, Público
    requiere_firma = db.Column(db.Boolean, default=False)
    firmado = db.Column(db.Boolean, default=False)
    firma_digital = db.Column(db.String(500))
    
    # Retención
    tabla_retencion_id = db.Column(db.Integer, db.ForeignKey('tabla_retencion.id'))
    fecha_destruccion = db.Column(db.DateTime)  # Calculada según tabla de retención
    
    # Auditoría
    creado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    modificado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_modificacion = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Control de acceso
    usuarios_con_acceso = db.Column(db.JSON)  # IDs de usuarios que pueden ver
    
    # Relaciones
    creado_por = db.relationship('Usuario', foreign_keys=[creado_por_id])
    modificado_por = db.relationship('Usuario', foreign_keys=[modificado_por_id])
    tabla_retencion = db.relationship('TablaRetencion', backref='documentos')
    documento_padre = db.relationship('DocumentoLegal', 
                                     foreign_keys=[documento_padre_id],
                                     remote_side=[id],
                                     backref='versiones')
    comentarios = db.relationship('ComentarioDocumento', backref='documento', 
                                 lazy='dynamic', cascade='all, delete-orphan')
    cambios = db.relationship('HistorialDocumento', backref='documento',
                             lazy='dynamic', cascade='all, delete-orphan')
    
    def crear_nueva_version(self, usuario_id, razon_cambio=''):
        """Crea nueva versión del documento actual"""
        # Marcar versión actual como anterior
        self.es_version_anterior = True
        
        # Crear nuevo documento como versión
        nueva_version = DocumentoLegal(
            consulta_id=self.consulta_id,
            nombre=self.nombre,
            tipo=self.tipo,
            contenido=self.contenido,
            ruta_archivo=self.ruta_archivo,
            numero_version=self.numero_version + 1,
            documento_padre_id=self.id if not self.documento_padre_id else self.documento_padre_id,
            creado_por_id=usuario_id,
            clasificacion=self.clasificacion,
            tabla_retencion_id=self.tabla_retencion_id
        )
        
        # Registrar cambio
        historial = HistorialDocumento(
            documento_id=self.id,
            usuario_id=usuario_id,
            razon_cambio=razon_cambio,
            version_anterior=self.numero_version,
            version_nueva=nueva_version.numero_version
        )
        
        db.session.add(nueva_version)
        db.session.add(historial)
        
        return nueva_version
    
    def calcular_hash(self, archivo_path):
        """Calcula SHA-256 del archivo para integridad"""
        import hashlib
        with open(archivo_path, 'rb') as f:
            self.hash_documento = hashlib.sha256(f.read()).hexdigest()
    
    def __repr__(self):
        return f'<DocumentoLegal {self.nombre} v{self.numero_version}>'


class HistorialDocumento(db.Model):
    """Historial de cambios en documentos"""
    __tablename__ = 'historial_documentos'
    
    id = db.Column(db.Integer, primary_key=True)
    documento_id = db.Column(db.Integer, db.ForeignKey('documentos_legales.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    accion = db.Column(db.String(50))  # creacion, modificacion, revision, aprobacion
    razon_cambio = db.Column(db.Text)
    version_anterior = db.Column(db.Integer)
    version_nueva = db.Column(db.Integer)
    
    fecha = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    detalles = db.Column(db.JSON)
    
    usuario = db.relationship('Usuario')


# ==================== COMENTARIOS COLABORATIVOS ====================

class ComentarioConsulta(db.Model):
    """Comentarios del equipo jurídico en consultas"""
    __tablename__ = 'comentarios_consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consultas_juridicas.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    contenido = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(30))  # Observacion, Sugerencia, Acuerdo, Advertencia
    prioridad = db.Column(db.String(20), default='Normal')
    
    # Para hilos de conversación
    responde_a_id = db.Column(db.Integer, db.ForeignKey('comentarios_consultas.id'))
    
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    fecha_edicion = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    usuario = db.relationship('Usuario', backref='comentarios_juridicos')
    respuestas = db.relationship('ComentarioConsulta', 
                                remote_side=[responde_a_id],
                                backref='comentario_padre')


class ComentarioDocumento(db.Model):
    """Comentarios en documentos específicos (anotaciones)"""
    __tablename__ = 'comentarios_documentos'
    
    id = db.Column(db.Integer, primary_key=True)
    documento_id = db.Column(db.Integer, db.ForeignKey('documentos_legales.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    contenido = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(30))  # Revision, Sugerencia, Pregunta, Aprobacion
    
    # Ubicación en el documento (opcional)
    linea_inicio = db.Column(db.Integer)
    linea_fin = db.Column(db.Integer)
    fragmento_texto = db.Column(db.String(500))  # Texto sobre el que comenta
    
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    usuario = db.relationship('Usuario')


# ==================== TABLA DE RETENCIÓN ====================

class TablaRetencion(db.Model):
    """
    Tabla de retención documental según:
    - Decreto 1072/2015 Art 2.2.3.1
    - ISO 27001, 45001
    - RGPD si aplica
    """
    __tablename__ = 'tabla_retencion'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)  # JUR-001, JUR-002, etc.
    
    # Clasificación
    tipo_documento = db.Column(db.String(200), nullable=False)  # Conceptos Jurídicos, Dictámenes, etc.
    descripcion = db.Column(db.Text)
    area_responsable = db.Column(db.String(100))
    
    # Tiempos de retención
    tiempo_retencion_anos = db.Column(db.Integer, nullable=False)  # Cuántos años conservar
    dias_retencion_activa = db.Column(db.Integer)  # Días en sistema activo antes de archivo
    dias_retencion_inactiva = db.Column(db.Integer)  # Días en archivo inactivo
    
    # Disposición final
    disposicion_final = db.Column(db.String(50))  # Destrucción, Conservación Permanente
    
    # Normativa
    normativa_aplicable = db.Column(db.JSON)  # Referencias legales
    
    # Control
    activa = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def calcular_fecha_destruccion(self, fecha_inicio):
        """Calcula cuándo debe destruirse el documento"""
        return fecha_inicio + timedelta(days=365 * self.tiempo_retencion_anos)


class TablasRetencionPredefinidas:
    """Tablas predefinidas según normativa SST Colombia 2025"""
    PREDEFINIDAS = [
        {
            'codigo': 'JUR-001',
            'tipo_documento': 'Conceptos Jurídicos',
            'tiempo_retencion_anos': 5,
            'disposicion_final': 'Destrucción',
            'normativa_aplicable': ['Decreto 1072/2015', 'Resolución 312/2019']
        },
        {
            'codigo': 'JUR-002',
            'tipo_documento': 'Dictámenes Especializados',
            'tiempo_retencion_anos': 10,
            'disposicion_final': 'Conservación Permanente',
            'normativa_aplicable': ['Decreto 1072/2015', 'Ley 985/2005']
        },
        {
            'codigo': 'JUR-003',
            'tipo_documento': 'Resoluciones de Conflictos',
            'tiempo_retencion_anos': 7,
            'disposicion_final': 'Destrucción',
            'normativa_aplicable': ['Código de Procedimiento Administrativo']
        },
        {
            'codigo': 'JUR-004',
            'tipo_documento': 'Contratos y Acuerdos',
            'tiempo_retencion_anos': 10,
            'disposicion_final': 'Conservación Permanente',
            'normativa_aplicable': ['Código Civil', 'Ley Comercial']
        },
        {
            'codigo': 'JUR-005',
            'tipo_documento': 'Documentos de Procesos Laborales',
            'tiempo_retencion_anos': 5,
            'disposicion_final': 'Destrucción',
            'normativa_aplicable': ['Código Sustantivo del Trabajo']
        }
    ]


# ==================== AUDITORÍA ====================

class AuditoriaConsulta(db.Model):
    """Auditoría completa de consultas jurídicas"""
    __tablename__ = 'auditoria_consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    consulta_id = db.Column(db.Integer, db.ForeignKey('consultas_juridicas.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    accion = db.Column(db.String(100), nullable=False)
    # cambio_estado, asignacion, creacion, resolucion, comentario, documento_agregado, etc.
    
    estado_anterior = db.Column(db.String(50))
    estado_nuevo = db.Column(db.String(50))
    
    razon = db.Column(db.Text)
    detalles = db.Column(db.JSON)  # Info adicional serializada
    
    fecha = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    ip_origen = db.Column(db.String(45))
    navegador = db.Column(db.String(500))
    
    usuario = db.relationship('Usuario')