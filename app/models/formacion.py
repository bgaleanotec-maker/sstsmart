from app import db
from app.tenancy import TenantMixin
from datetime import datetime


# Tabla de asociación para Matrículas (Muchos a Muchos)
matriculas = db.Table('matriculas',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('curso_id', db.Integer, db.ForeignKey('cursos.id'), primary_key=True),
    db.Column('fecha_matricula', db.DateTime, default=datetime.utcnow)
)

class Curso(TenantMixin, db.Model):
    """Cursos de formación SST"""
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    contenido_html = db.Column(db.Text)  # Contenido del curso o embed
    
    # Nuevos campos para "Netflix Style" y PDFs
    tipo_contenido = db.Column(db.String(20), default='video') # 'video', 'pdf', 'mixto'
    categoria = db.Column(db.String(100), default='General') # Ej: 'Alturas', 'Ergonomía', 'Fuego'
    imagen_portada = db.Column(db.String(500)) # URL de la imagen thumbnail
    pdf_url = db.Column(db.String(500)) # URL del PDF si es lectura
    
    video_url = db.Column(db.String(500)) # URL opcional de video
    duracion_horas = db.Column(db.Integer, default=1)
    puntaje_maximo = db.Column(db.Integer, default=100)
    estado = db.Column(db.String(20), default='Activo') # Activo, Inactivo
    
    examenes = db.relationship('Examen', backref='curso', lazy=True, cascade='all, delete-orphan')
    estudiantes = db.relationship('Usuario', secondary=matriculas, lazy='subquery',
        backref=db.backref('cursos_matriculados', lazy=True))
    
    def __repr__(self):
        return f'<Curso {self.titulo}>'

class Examen(db.Model):
    """Examen asociado a un curso"""
    __tablename__ = 'examenes'
    id = db.Column(db.Integer, primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    porcentaje_aprobacion = db.Column(db.Integer, default=70) # Ej: 70% para pasar
    puntaje_total = db.Column(db.Integer, default=100)
    
    preguntas = db.relationship('Pregunta', backref='examen', lazy=True, cascade='all, delete-orphan')
    intentos = db.relationship('IntentoExamen', backref='examen', lazy=True, cascade='all, delete-orphan')

class Pregunta(db.Model):
    """Preguntas del examen"""
    __tablename__ = 'preguntas'
    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey('examenes.id'), nullable=False)
    texto_pregunta = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(20), default='seleccion_multiple') # seleccion_multiple, verdadero_falso
    puntaje = db.Column(db.Integer, default=10)
    
    opciones = db.relationship('Opcion', backref='pregunta', lazy=True, cascade='all, delete-orphan')

class Opcion(db.Model):
    """Opciones de respuesta para una pregunta"""
    __tablename__ = 'opciones'
    id = db.Column(db.Integer, primary_key=True)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('preguntas.id'), nullable=False)
    texto_opcion = db.Column(db.String(500), nullable=False)
    es_correcta = db.Column(db.Boolean, default=False)

class IntentoExamen(db.Model):
    """Registro de intentos de examen por usuario"""
    __tablename__ = 'intentos_examen'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    examen_id = db.Column(db.Integer, db.ForeignKey('examenes.id'), nullable=False)
    fecha_intento = db.Column(db.DateTime, default=datetime.utcnow)
    puntaje_obtenido = db.Column(db.Float, default=0)
    aprobado = db.Column(db.Boolean, default=False)
    
    usuario = db.relationship('Usuario', backref=db.backref('intentos_examen', lazy=True))

class ProgresoFormacion(db.Model):
    """Resumen del progreso de formación del usuario"""
    __tablename__ = 'progreso_formacion'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, unique=True)
    total_cursos_asignados = db.Column(db.Integer, default=0)
    total_cursos_completados = db.Column(db.Integer, default=0)
    puntaje_global_sst = db.Column(db.Float, default=0.0) # Score calculado
    ultimo_calculo = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('Usuario', backref=db.backref('progreso_formacion', uselist=False))
