"""Modelo Empresa — la unidad de tenancy del SaaS.

Esquema según docs/03-arquitectura/01-arquitectura-saas-multitenant.md §1.2.
OJO: el Decreto 957/2019 clasifica el tamaño por INGRESOS; la Res. 0312/2019
asigna el régimen de estándares por TRABAJADORES y clase de riesgo. Se guardan
por separado a propósito — no unificar.
"""
from app import db
from datetime import datetime


class Empresa(db.Model):
    __tablename__ = 'empresas'

    id = db.Column(db.Integer, primary_key=True)
    nit = db.Column(db.String(20), unique=True, nullable=False)
    razon_social = db.Column(db.String(255), nullable=False)
    ciiu = db.Column(db.String(10))
    clase_riesgo = db.Column(db.SmallInteger, default=1)      # 1..5 (Decreto 1607/2002)
    num_trabajadores = db.Column(db.Integer, nullable=False, default=1)
    tamano_dec957 = db.Column(db.String(20))                  # micro/pequeña/mediana/grande (por ingresos)
    regimen_estandares = db.Column(db.SmallInteger)           # 7 | 21 | 60 (derivado)
    num_vehiculos = db.Column(db.Integer, default=0)          # disparadores upsell PESV
    num_conductores = db.Column(db.Integer, default=0)
    # Res. 0312/2019 art. 3 num. 8: las unidades de producción agropecuaria de
    # <10 trabajadores riesgo I-III cumplen 21 estándares, NO 7
    unidad_agropecuaria = db.Column(db.Boolean, default=False)

    plan = db.Column(db.String(30), default='beta')
    estado = db.Column(db.String(20), default='activa')
    creada_en = db.Column(db.DateTime, default=datetime.utcnow)

    def calcular_regimen(self):
        """Régimen de estándares mínimos según Res. 0312/2019 (arts. 3, 9, 16):
        7  → ≤10 trabajadores y riesgo I-III
        21 → 11-50 trabajadores y riesgo I-III
        21 → unidad agropecuaria de ≤10 trabajadores riesgo I-III (art. 3 num. 8)
        60 → >50 trabajadores o riesgo IV-V (cualquier tamaño)
        """
        if (self.clase_riesgo or 1) >= 4:
            self.regimen_estandares = 60
        elif (self.num_trabajadores or 1) <= 10:
            self.regimen_estandares = 21 if self.unidad_agropecuaria else 7
        elif self.num_trabajadores <= 50:
            self.regimen_estandares = 21
        else:
            self.regimen_estandares = 60
        return self.regimen_estandares

    def __repr__(self):
        return f'<Empresa {self.nit} {self.razon_social}>'
