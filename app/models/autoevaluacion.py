"""Autoevaluación de Estándares Mínimos — Resolución 0312 de 2019.

Una autoevaluación por empresa y año. Cada respuesta califica un ítem de la
tabla de valores (app/data/estandares_0312.py). El plan de mejoramiento se
deriva de los ítems NO CUMPLE.
"""
from app import db
from app.tenancy import TenantMixin
from datetime import datetime


class Autoevaluacion(TenantMixin, db.Model):
    __tablename__ = 'autoevaluaciones'
    __table_args__ = (
        db.UniqueConstraint('empresa_id', 'anio', name='uq_autoeval_empresa_anio'),
    )

    id = db.Column(db.Integer, primary_key=True)
    anio = db.Column(db.Integer, nullable=False)          # vigencia evaluada
    regimen = db.Column(db.SmallInteger, nullable=False)  # 7 | 21 | 60 al momento de crearla

    estado = db.Column(db.String(20), default='EN_CURSO')  # EN_CURSO | CERRADA
    puntaje_total = db.Column(db.Float)
    clasificacion = db.Column(db.String(20))               # CRITICO | MODERADO | ACEPTABLE

    creada_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_cierre = db.Column(db.DateTime)

    respuestas = db.relationship('RespuestaAutoevaluacion', backref='autoevaluacion',
                                 lazy='dynamic', cascade='all, delete-orphan')
    acciones = db.relationship('AccionMejora', backref='autoevaluacion',
                               lazy='dynamic', cascade='all, delete-orphan')
    creada_por = db.relationship('Usuario')

    def __repr__(self):
        return f'<Autoevaluacion {self.anio} régimen {self.regimen}>'


class RespuestaAutoevaluacion(db.Model):
    """Calificación de un ítem. El catálogo vive en código, no en BD: aquí solo
    se guarda el código del ítem y la calificación."""
    __tablename__ = 'respuestas_autoevaluacion'
    __table_args__ = (
        db.UniqueConstraint('autoevaluacion_id', 'item_codigo', name='uq_resp_item'),
    )

    id = db.Column(db.Integer, primary_key=True)
    autoevaluacion_id = db.Column(db.Integer, db.ForeignKey('autoevaluaciones.id'),
                                  nullable=False, index=True)
    item_codigo = db.Column(db.String(10), nullable=False)   # p. ej. "3.1.4"
    calificacion = db.Column(db.String(12), default='PENDIENTE')
    # CUMPLE | NO_CUMPLE | NO_APLICA | PENDIENTE
    justificacion = db.Column(db.Text)                        # obligatoria para NO_APLICA
    puntaje_obtenido = db.Column(db.Float, default=0.0)
    actualizada_en = db.Column(db.DateTime, default=datetime.utcnow,
                               onupdate=datetime.utcnow)


class AccionMejora(TenantMixin, db.Model):
    """Plan de mejoramiento derivado de la autoevaluación (art. 28)."""
    __tablename__ = 'acciones_mejora'

    id = db.Column(db.Integer, primary_key=True)
    autoevaluacion_id = db.Column(db.Integer, db.ForeignKey('autoevaluaciones.id'),
                                  nullable=False, index=True)
    item_codigo = db.Column(db.String(10), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_limite = db.Column(db.Date)
    estado = db.Column(db.String(20), default='Abierta')  # Abierta | En_Proceso | Cerrada
    creada_en = db.Column(db.DateTime, default=datetime.utcnow)

    responsable = db.relationship('Usuario')
