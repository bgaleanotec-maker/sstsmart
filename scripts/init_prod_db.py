# -*- coding: utf-8 -*-
"""Inicialización idempotente de la base de datos (preDeployCommand en Render).

- Crea tablas nuevas (create_all es aditivo: no toca tablas existentes).
- Siembra la matriz legal SST 2026.
- Garantiza la empresa 1 y el usuario admin inicial.
- Backfill de empresa_id (fase expand del plan expand/contract).

Nota: cambios de columnas sobre tablas existentes requieren migración formal
(Flask-Migrate); este script cubre el arranque y las tablas nuevas.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db  # noqa: E402


def main():
    config = os.getenv('FLASK_CONFIG', 'production')
    app = create_app(config)
    with app.app_context():
        from app.models import Empresa, Usuario
        from sqlalchemy import text

        db.create_all()

        # Empresa 1 (tenant por defecto para datos históricos)
        empresa = Empresa.query.first()
        if not empresa:
            empresa = Empresa(nit='000000000', razon_social='Mi Empresa',
                              num_trabajadores=10, clase_riesgo=1)
            empresa.calcular_regimen()
            db.session.add(empresa)
            db.session.commit()
            print(f"Empresa inicial creada (id={empresa.id})")

        # Admin inicial
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@sst.local')
        admin = Usuario.query.filter_by(email=admin_email).first()
        if not admin:
            admin = Usuario(email=admin_email, nombre_completo='Administrador SST',
                            rol='Admin', activo=True, empresa_id=empresa.id)
            admin.set_password(os.getenv('ADMIN_PASSWORD', 'admin123'))
            db.session.add(admin)
            db.session.commit()
            print(f"Admin creado: {admin_email}")

        # Backfill de empresa_id en tablas tenant (solo filas huérfanas)
        tablas_tenant = [
            'usuarios', 'empleados', 'condiciones_inseguras', 'eventos',
            'riesgo_matriz', 'controles', 'requisitos_legales',
            'consultas_juridicas', 'cursos', 'gestion_reportes',
            'autoevaluaciones', 'acciones_mejora', 'empresa_modulos',
        ]
        for tabla in tablas_tenant:
            try:
                r = db.session.execute(text(
                    f"UPDATE {tabla} SET empresa_id = :eid WHERE empresa_id IS NULL"
                ), {'eid': empresa.id})
                if r.rowcount:
                    print(f"Backfill {tabla}: {r.rowcount} filas")
            except Exception as e:
                print(f"AVISO {tabla}: {e}")
                db.session.rollback()
        db.session.commit()

        # Todos los módulos activos para la empresa inicial
        from app.models import EmpresaModulo
        from app.data.modulos import MODULOS
        for codigo in MODULOS:
            if not EmpresaModulo.query.filter_by(empresa_id=empresa.id, modulo=codigo).first():
                db.session.add(EmpresaModulo(empresa_id=empresa.id, modulo=codigo, activo=True))
        db.session.commit()

        # Matriz legal 2026
        from scripts.seed_matriz_legal import seed
        # el seed corre con contexto de tenant implícito nulo → asignamos empresa
        from app.tenancy import set_empresa
        set_empresa(empresa.id)
        seed()
        set_empresa(None)

        print("init_prod_db: OK")


if __name__ == '__main__':
    main()
