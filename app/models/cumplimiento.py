# -*- coding: utf-8 -*-
"""Modelos del módulo de cumplimiento (SARLAFT, PTEE, SAGRILAFT, datos personales).

Todos llevan TenantMixin (regla dura 5) y están registrados en
tests/test_aislamiento_tenants.py, scripts/init_prod_db.py y scripts/rls_postgres.sql.
El catálogo de programas vive en app/data/programas_cumplimiento.py; aquí solo
se guarda lo que la empresa decide y hace.
"""
from datetime import datetime, date

from app import db
from app.tenancy import TenantMixin

ESTADOS_REQUISITO = ('pendiente', 'en_curso', 'cumplido', 'no_aplica')
ESTADOS_REPORTE = ('pendiente', 'presentado', 'no_aplica')
NIVELES_RIESGO = ('bajo', 'medio', 'alto')
RESULTADOS_VERIFICACION = ('por_revisar', 'sin_coincidencia', 'coincidencia')


class ProgramaCumplimiento(TenantMixin, db.Model):
    """Un programa del catálogo activado por la empresa, con su régimen y su oficial."""
    __tablename__ = 'cumpl_programas'
    __table_args__ = (db.UniqueConstraint('empresa_id', 'codigo', name='uq_cumpl_programa'),)

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(40), nullable=False, index=True)     # clave de PROGRAMAS
    regimen = db.Column(db.String(30), nullable=False)
    estado = db.Column(db.String(20), default='activo', nullable=False)  # activo | suspendido
    fecha_activacion = db.Column(db.Date, default=date.today, nullable=False)

    # Oficial o responsable de cumplimiento
    oficial_nombre = db.Column(db.String(150))
    oficial_documento = db.Column(db.String(30))
    oficial_correo = db.Column(db.String(150))
    oficial_tipo = db.Column(db.String(20))          # interno | externo
    suplente_nombre = db.Column(db.String(150))
    acta_designacion = db.Column(db.String(100))
    fecha_designacion = db.Column(db.Date)
    registro_sirel = db.Column(db.Boolean, default=False)
    fecha_aprobacion_politica = db.Column(db.Date)
    notas = db.Column(db.Text)

    creado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    requisitos = db.relationship('RequisitoCumplimiento', back_populates='programa',
                                 cascade='all, delete-orphan', order_by='RequisitoCumplimiento.id')
    riesgos = db.relationship('RiesgoCumplimiento', back_populates='programa',
                              cascade='all, delete-orphan')
    reportes = db.relationship('ReporteCumplimiento', back_populates='programa',
                               cascade='all, delete-orphan', order_by='ReporteCumplimiento.fecha_limite')

    @property
    def info(self):
        from app.data.programas_cumplimiento import PROGRAMAS
        return PROGRAMAS.get(self.codigo, {})

    @property
    def nombre(self):
        return self.info.get('nombre', self.codigo)

    @property
    def nombre_regimen(self):
        return self.info.get('regimenes', {}).get(self.regimen, self.regimen)

    def __repr__(self):
        return f'<ProgramaCumplimiento {self.codigo}/{self.regimen}>'


class RequisitoCumplimiento(TenantMixin, db.Model):
    """Estado y evidencia de un requisito del catálogo para un programa activado."""
    __tablename__ = 'cumpl_requisitos'
    __table_args__ = (db.UniqueConstraint('programa_id', 'codigo', name='uq_cumpl_requisito'),)

    id = db.Column(db.Integer, primary_key=True)
    programa_id = db.Column(db.Integer, db.ForeignKey('cumpl_programas.id'), nullable=False, index=True)
    codigo = db.Column(db.String(40), nullable=False)
    estado = db.Column(db.String(20), default='pendiente', nullable=False)
    evidencia = db.Column(db.Text)                 # descripción, número de acta, enlace
    fecha_cumplimiento = db.Column(db.Date)
    proxima_revision = db.Column(db.Date)          # para requisitos periódicos
    responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    programa = db.relationship('ProgramaCumplimiento', back_populates='requisitos')
    responsable = db.relationship('Usuario', foreign_keys=[responsable_id])

    @property
    def info(self):
        from app.data.programas_cumplimiento import requisito_info
        return requisito_info(self.programa.codigo, self.codigo)

    @property
    def nombre(self):
        return self.info['nombre']

    def vencido(self, hoy=None):
        hoy = hoy or date.today()
        return bool(self.proxima_revision and self.proxima_revision < hoy
                    and self.estado != 'no_aplica')

    def __repr__(self):
        return f'<RequisitoCumplimiento {self.codigo} {self.estado}>'


class Contraparte(TenantMixin, db.Model):
    """Tercero vinculado a la empresa con su debida diligencia: cliente, proveedor,
    empleado, socio, conductor o propietario de vehículo. Es compartida por todos
    los programas de la empresa (un mismo tercero se verifica una vez)."""
    __tablename__ = 'cumpl_contrapartes'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(30), nullable=False, default='cliente')
    nombre = db.Column(db.String(200), nullable=False)
    tipo_documento = db.Column(db.String(10), default='NIT')     # NIT | CC | CE | PA
    documento = db.Column(db.String(30), index=True)
    pais = db.Column(db.String(60), default='Colombia')
    actividad = db.Column(db.String(150))
    pep = db.Column(db.Boolean, default=False)                   # persona expuesta políticamente
    nivel_riesgo = db.Column(db.String(10), default='bajo')
    fecha_vinculacion = db.Column(db.Date, default=date.today)

    ultima_verificacion = db.Column(db.Date)
    resultado_verificacion = db.Column(db.String(20), default='por_revisar')
    fuente_verificacion = db.Column(db.String(200))      # 'ONU lista consolidada (automática)', 'OFAC (manual)'...
    detalle_verificacion = db.Column(db.Text)            # coincidencias encontradas, para auditoría
    proxima_verificacion = db.Column(db.Date)
    senales_alerta = db.Column(db.Text)
    estado = db.Column(db.String(20), default='activa', nullable=False)   # activa | bloqueada | retirada
    notas = db.Column(db.Text)

    creado_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def verificacion_vencida(self, hoy=None):
        hoy = hoy or date.today()
        if self.resultado_verificacion == 'por_revisar':
            return True
        return bool(self.proxima_verificacion and self.proxima_verificacion < hoy)

    def __repr__(self):
        return f'<Contraparte {self.tipo} {self.nombre}>'


class RiesgoCumplimiento(TenantMixin, db.Model):
    """Fila de la matriz de riesgos de un programa (LA/FT/FPADM, corrupción o datos)."""
    __tablename__ = 'cumpl_riesgos'

    id = db.Column(db.Integer, primary_key=True)
    programa_id = db.Column(db.Integer, db.ForeignKey('cumpl_programas.id'), nullable=False, index=True)
    factor = db.Column(db.String(20), nullable=False, default='contraparte')
    descripcion = db.Column(db.String(300), nullable=False)
    probabilidad = db.Column(db.SmallInteger, default=3)       # 1..5
    impacto = db.Column(db.SmallInteger, default=3)            # 1..5
    controles = db.Column(db.Text)
    probabilidad_residual = db.Column(db.SmallInteger)
    impacto_residual = db.Column(db.SmallInteger)
    responsable_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    programa = db.relationship('ProgramaCumplimiento', back_populates='riesgos')
    responsable = db.relationship('Usuario', foreign_keys=[responsable_id])

    @property
    def inherente(self):
        return (self.probabilidad or 0) * (self.impacto or 0)

    @property
    def residual(self):
        p = self.probabilidad_residual if self.probabilidad_residual else self.probabilidad
        i = self.impacto_residual if self.impacto_residual else self.impacto
        return (p or 0) * (i or 0)

    @property
    def nivel(self):
        from app.services.cumplimiento_service import nivel_riesgo
        return nivel_riesgo(self.residual)

    def __repr__(self):
        return f'<RiesgoCumplimiento {self.factor}: {self.descripcion[:30]}>'


class ReporteCumplimiento(TenantMixin, db.Model):
    """Un reporte con fecha límite (a la Supertransporte, a la SIC, a la UIAF)."""
    __tablename__ = 'cumpl_reportes'
    __table_args__ = (db.UniqueConstraint('programa_id', 'codigo', 'fecha_limite', name='uq_cumpl_reporte'),)

    id = db.Column(db.Integer, primary_key=True)
    programa_id = db.Column(db.Integer, db.ForeignKey('cumpl_programas.id'), nullable=False, index=True)
    codigo = db.Column(db.String(40), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    fecha_limite = db.Column(db.Date, nullable=False, index=True)
    fecha_presentacion = db.Column(db.Date)
    radicado = db.Column(db.String(100))
    estado = db.Column(db.String(20), default='pendiente', nullable=False)
    verificado = db.Column(db.Boolean, default=False)   # la fecha está confirmada con la fuente oficial
    notas = db.Column(db.Text)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)

    programa = db.relationship('ProgramaCumplimiento', back_populates='reportes')

    def dias_restantes(self, hoy=None):
        hoy = hoy or date.today()
        return (self.fecha_limite - hoy).days

    def __repr__(self):
        return f'<ReporteCumplimiento {self.codigo} {self.fecha_limite} {self.estado}>'
