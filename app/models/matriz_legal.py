from app import db
from app.tenancy import TenantMixin
from datetime import datetime
from flask_login import current_user
import enum

class EstadoRequisito(enum.Enum):
    PENDIENTE = "Pendiente"
    CUMPLE = "Cumple"
    NO_CUMPLE = "No Cumple"
    EN_PROCESO = "En Proceso"

class ProbabilidadSancion(enum.Enum):
    BAJA = "Baja"   # 1
    MEDIA = "Media" # 2
    ALTA = "Alta"   # 3

class RequisitoLegal(TenantMixin, db.Model):
    __tablename__ = 'requisitos_legales'

    id = db.Column(db.Integer, primary_key=True)
    norma = db.Column(db.String(255), nullable=False)  # Ej: Ley 9 de 1979
    articulo = db.Column(db.String(100), nullable=False) # Ej: Art. 120
    descripcion = db.Column(db.Text, nullable=False)
    entidad = db.Column(db.String(100)) # Ej: Congreso, MinTrabajo
    anio = db.Column(db.Integer)
    
    estado = db.Column(db.Enum(EstadoRequisito), default=EstadoRequisito.PENDIENTE)
    
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    valoraciones = db.relationship('ValoracionJuridica', backref='requisito', lazy=True, cascade="all, delete-orphan")
    evidencias = db.relationship('EvidenciaLegal', backref='requisito', lazy=True, cascade="all, delete-orphan")
    logs = db.relationship('LogMatrizLegal', backref='requisito', lazy=True, cascade="all, delete-orphan")

    def log_accion(self, usuario_id, accion, detalles):
        log = LogMatrizLegal(
            requisito_id=self.id,
            usuario_id=usuario_id,
            accion=accion,
            detalles=detalles
        )
        db.session.add(log)

class ValoracionJuridica(db.Model):
    __tablename__ = 'valoraciones_juridicas'

    id = db.Column(db.Integer, primary_key=True)
    requisito_id = db.Column(db.Integer, db.ForeignKey('requisitos_legales.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False) # Abogado que evalúa
    
    puntuacion_cumplimiento = db.Column(db.Integer) # 0-100
    probabilidad_sancion = db.Column(db.Enum(ProbabilidadSancion)) 
    impacto_financiero = db.Column(db.Float) # En pesos o unidades monetarias
    concepto_final = db.Column(db.Text)
    
    fecha_valoracion = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def nivel_riesgo_total(self):
        """
        Cálculo del riesgo forense.
        Probabilidad (1,2,3) * Impacto
        """
        prob_map = {
            ProbabilidadSancion.BAJA: 1,
            ProbabilidadSancion.MEDIA: 2,
            ProbabilidadSancion.ALTA: 3
        }
        factor = prob_map.get(self.probabilidad_sancion, 1)
        # Si no hay impacto definido, asumimos 1 para no anular, o 0 si se prefiere.
        impacto = self.impacto_financiero if self.impacto_financiero else 0
        return factor * impacto

    @property
    def color_semaforo(self):
        # Esta lógica puede ser ajustada según las necesidades del negocio
        riesgo = self.nivel_riesgo_total
        # Ejemplo de umbrales arbitrarios, ajustar según "Salario Mínimo Legal" o política de la empresa
        if self.probabilidad_sancion == ProbabilidadSancion.ALTA and riesgo > 10000000: # Riesgo alto > 10M
            return "red"
        elif self.probabilidad_sancion == ProbabilidadSancion.MEDIA or riesgo > 1000000:
            return "yellow"
        else:
            return "green"

class EvidenciaLegal(db.Model):
    __tablename__ = 'evidencias_legales'

    id = db.Column(db.Integer, primary_key=True)
    requisito_id = db.Column(db.Integer, db.ForeignKey('requisitos_legales.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    archivo_path = db.Column(db.String(255), nullable=False)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    version = db.Column(db.Integer, default=1)
    descripcion_cambio = db.Column(db.String(255)) # Razón de la nueva versión
    
    fecha_carga = db.Column(db.DateTime, default=datetime.utcnow)

class LogMatrizLegal(db.Model):
    __tablename__ = 'logs_matriz_legal'

    id = db.Column(db.Integer, primary_key=True)
    requisito_id = db.Column(db.Integer, db.ForeignKey('requisitos_legales.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    
    accion = db.Column(db.String(50), nullable=False) # CREACION, MODIFICACION, EVALUACION, EVIDENCIA
    detalles = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
