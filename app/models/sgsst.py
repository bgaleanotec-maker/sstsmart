"""Núcleo documental del SG-SST (Decreto 1072/2015).

- PoliticaSST: política escrita, firmada y actualizada al menos cada año
  (arts. 2.2.4.6.5 y 2.2.4.6.6). Versionada por año.
- PlanTrabajoActividad: plan anual de trabajo con objetivos, responsables y
  cronograma (art. 2.2.4.6.17; estándar 2.4.1 de la Res. 0312/2019).
- EntregaEPP: kardex de entrega de elementos de protección personal
  (art. 2.2.4.6.24). Los cuatro deberes jurisprudenciales en EPP son
  suministrar, capacitar, verificar y reponer: este kardex es la prueba
  documental de defensa ante una acción de culpa patronal (art. 216 CST).
"""
from app import db
from app.tenancy import TenantMixin
from datetime import datetime, date


class PoliticaSST(TenantMixin, db.Model):
    __tablename__ = 'politicas_sst'
    __table_args__ = (
        db.UniqueConstraint('empresa_id', 'anio', name='uq_politica_empresa_anio'),
    )

    id = db.Column(db.Integer, primary_key=True)
    anio = db.Column(db.Integer, nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    version = db.Column(db.Integer, default=1)

    firmada_por = db.Column(db.String(150))       # representante legal
    cargo_firmante = db.Column(db.String(100))
    fecha_firma = db.Column(db.Date)
    divulgada = db.Column(db.Boolean, default=False)
    fecha_divulgacion = db.Column(db.Date)

    creada_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    creada_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizada_en = db.Column(db.DateTime, default=datetime.utcnow,
                               onupdate=datetime.utcnow)

    @property
    def vigente(self):
        """La política debe revisarse al menos una vez al año."""
        return self.anio >= date.today().year

    def __repr__(self):
        return f'<PoliticaSST {self.anio} v{self.version}>'


class PlanTrabajoActividad(TenantMixin, db.Model):
    __tablename__ = 'plan_trabajo_actividades'

    id = db.Column(db.Integer, primary_key=True)
    anio = db.Column(db.Integer, nullable=False, index=True)
    objetivo = db.Column(db.String(300), nullable=False)
    actividad = db.Column(db.String(300), nullable=False)
    responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    recursos = db.Column(db.String(200))
    fecha_programada = db.Column(db.Date)
    fecha_ejecucion = db.Column(db.Date)
    estado = db.Column(db.String(20), default='Programada')
    # Programada | En_Ejecucion | Ejecutada | Vencida (derivado en vista)
    evidencia = db.Column(db.String(500))
    creada_en = db.Column(db.DateTime, default=datetime.utcnow)

    responsable = db.relationship('Usuario')

    @property
    def vencida(self):
        return (self.estado != 'Ejecutada' and self.fecha_programada
                and self.fecha_programada < date.today())

    def __repr__(self):
        return f'<PlanTrabajoActividad {self.anio}: {self.actividad[:30]}>'


class EntregaEPP(TenantMixin, db.Model):
    __tablename__ = 'entregas_epp'

    id = db.Column(db.Integer, primary_key=True)
    trabajador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    elemento = db.Column(db.String(150), nullable=False)   # casco, arnés, guantes...
    referencia = db.Column(db.String(100))                  # marca / modelo
    certificacion = db.Column(db.String(100))               # NTC / ANSI / EN aplicable
    cantidad = db.Column(db.Integer, default=1)

    fecha_entrega = db.Column(db.Date, default=date.today, nullable=False)
    vida_util_meses = db.Column(db.Integer)                 # para alerta de reposición
    fecha_reposicion = db.Column(db.Date)                   # próxima reposición estimada

    capacitado_en_uso = db.Column(db.Boolean, default=False)  # deber 2: capacitar
    constancia = db.Column(db.String(300))                    # acta / soporte de recibido
    observaciones = db.Column(db.Text)

    entregado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    creada_en = db.Column(db.DateTime, default=datetime.utcnow)

    trabajador = db.relationship('Usuario', foreign_keys=[trabajador_id])
    entregado_por = db.relationship('Usuario', foreign_keys=[entregado_por_id])

    @property
    def reposicion_vencida(self):
        return self.fecha_reposicion and self.fecha_reposicion < date.today()

    def __repr__(self):
        return f'<EntregaEPP {self.elemento} → usuario {self.trabajador_id}>'
