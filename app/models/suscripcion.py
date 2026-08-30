"""Suscripción por módulos: qué contrató cada empresa y a qué precio."""
from app import db
from app.tenancy import TenantMixin
from datetime import datetime


class EmpresaModulo(TenantMixin, db.Model):
    __tablename__ = 'empresa_modulos'
    __table_args__ = (
        db.UniqueConstraint('empresa_id', 'modulo', name='uq_empresa_modulo'),
    )

    id = db.Column(db.Integer, primary_key=True)
    modulo = db.Column(db.String(30), nullable=False)      # codigo del catálogo
    activo = db.Column(db.Boolean, default=True)
    # NULL = usa el precio de lista del catálogo; valor = precio pactado
    precio_pactado = db.Column(db.Integer)
    activado_en = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<EmpresaModulo {self.empresa_id}:{self.modulo} {"on" if self.activo else "off"}>'
