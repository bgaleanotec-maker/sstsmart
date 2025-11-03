from app import db
from datetime import datetime

class CategoriaArea(db.Model):
    """Categorías de áreas (Industrial, Mantenimiento, Oficina, etc)"""
    __tablename__ = 'categorias_areas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    icono = db.Column(db.String(50))
    color = db.Column(db.String(7), default='#3b82f6')
    activa = db.Column(db.Boolean, default=True)
    creada_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    dependencias = db.relationship('Dependencia', backref='categoria', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<CategoriaArea {self.nombre}>'

class Dependencia(db.Model):
    """Dependencias/Ubicaciones dentro de la empresa"""
    __tablename__ = 'dependencias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    direccion = db.Column(db.String(300))
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias_areas.id'), nullable=False)
    activa = db.Column(db.Boolean, default=True)
    creada_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    roles_vinculados = db.relationship('RolSST', secondary='dependencia_rol', backref='dependencias')
    
    def __repr__(self):
        return f'<Dependencia {self.nombre}>'

class RolSST(db.Model):
    """Roles específicos para SST"""
    __tablename__ = 'roles_sst'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    permisos = db.Column(db.JSON)
    activo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<RolSST {self.nombre}>'

# Tabla muchos a muchos: Dependencia - RolSST
dependencia_rol = db.Table(
    'dependencia_rol',
    db.Column('dependencia_id', db.Integer, db.ForeignKey('dependencias.id'), primary_key=True),
    db.Column('rol_id', db.Integer, db.ForeignKey('roles_sst.id'), primary_key=True)
)

class TipoReporte(db.Model):
    """Tipos de reportes según URF"""
    __tablename__ = 'tipos_reportes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    requiere_investigacion = db.Column(db.Boolean, default=True)
    activo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<TipoReporte {self.nombre}>'

class TipoEvidencia(db.Model):
    """Tipos de evidencia observada"""
    __tablename__ = 'tipos_evidencia'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    codigo = db.Column(db.String(30))
    activo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<TipoEvidencia {self.nombre}>'

class MetodologiaInvestigacion(db.Model):
    """Metodologías de investigación"""
    __tablename__ = 'metodologias_investigacion'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    template = db.Column(db.JSON)
    activa = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<MetodologiaInvestigacion {self.nombre}>'