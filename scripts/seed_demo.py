# -*- coding: utf-8 -*-
"""Datos de demostración para desarrollo y QA del rediseño (idempotente).

Crea, si no existen: la empresa demo (46 trabajadores, riesgo IV → 60
estándares), el admin, una autoevaluación 2026 cerrada con incumplimientos
(puntaje moderadamente aceptable), plan anual con una actividad vencida y
otra próxima, kardex EPP con una reposición vencida, un reporte de condición
insegura, un riesgo con su control, una consulta jurídica y un curso con
examen. Además corre la siembra de la matriz legal.

Uso: SCHEDULER_ENABLED=0 venv/Scripts/python.exe scripts/seed_demo.py
NO usar en producción: son datos ficticios.
"""
import os
import sys
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db  # noqa: E402


def main():
    app = create_app(os.getenv('FLASK_CONFIG', 'development'))
    with app.app_context():
        from app.models import (Empresa, Usuario, CondicionInsegura, RiesgoMatriz,
                                Control, ConsultaJuridica, Curso, Examen, Pregunta,
                                Opcion, EmpresaModulo)
        from app.models.autoevaluacion import Autoevaluacion
        from app.models.sgsst import PlanTrabajoActividad, EntregaEPP
        from app.data.modulos import MODULOS
        from app.services import autoevaluacion_service as svc
        from app.tenancy import set_empresa

        db.create_all()
        hoy = date.today()

        empresa = Empresa.query.filter_by(nit='900123456').first()
        if not empresa:
            empresa = Empresa(nit='900123456', razon_social='Transportes El Recreo S.A.S.',
                              ciiu='4923', num_trabajadores=46, clase_riesgo=4)
            empresa.calcular_regimen()
            db.session.add(empresa)
            db.session.commit()
        # Buscar usuarios SIN filtro de tenant (pueden venir de otra empresa)
        set_empresa(None)
        admin = Usuario.query.filter_by(email='admin@sst.local').first()
        if not admin:
            admin = Usuario(email='admin@sst.local', nombre_completo='Ana Rojas',
                            rol='Admin', activo=True, empresa_id=empresa.id)
            admin.set_password('admin123')
            db.session.add(admin)
        else:
            admin.empresa_id = empresa.id
        trabajador = Usuario.query.filter_by(email='operario@demo.local').first()
        set_empresa(empresa.id)
        if not trabajador:
            trabajador = Usuario(email='operario@demo.local', nombre_completo='Carlos Pérez',
                                 rol='Empleado', activo=True, empresa_id=empresa.id)
            db.session.add(trabajador)
            trabajador.set_password('operario123')
            db.session.add(trabajador)
        db.session.commit()

        for codigo in MODULOS:
            if not EmpresaModulo.query.filter_by(modulo=codigo).first():
                db.session.add(EmpresaModulo(modulo=codigo, activo=True))
        db.session.commit()

        if not Autoevaluacion.query.filter_by(anio=hoy.year).first():
            a = svc.crear_autoevaluacion(empresa, hoy.year, admin.id)
            incumplidos = {'5.1.1', '5.1.2', '4.1.1', '4.1.4', '3.1.4', '2.5.1', '1.2.3', '6.1.2', '7.1.1'}
            for r in a.respuestas:
                r.calificacion = 'NO_CUMPLE' if r.item_codigo in incumplidos else 'CUMPLE'
            svc.cerrar_autoevaluacion(a)   # ≈ 72 puntos

        if not PlanTrabajoActividad.query.filter_by(anio=hoy.year).first():
            db.session.add_all([
                PlanTrabajoActividad(anio=hoy.year, objetivo='Preparación ante emergencias',
                                     actividad='Simulacro de evacuación del plan de emergencias',
                                     responsable_id=admin.id, fecha_programada=hoy + timedelta(days=12)),
                PlanTrabajoActividad(anio=hoy.year, objetivo='Capacitación',
                                     actividad='Reinducción en SST a todo el personal',
                                     responsable_id=admin.id, fecha_programada=hoy - timedelta(days=20)),
                PlanTrabajoActividad(anio=hoy.year, objetivo='Capacitación',
                                     actividad='Inducción a nuevos ingresos',
                                     responsable_id=admin.id, fecha_programada=hoy - timedelta(days=60),
                                     estado='Ejecutada', fecha_ejecucion=hoy - timedelta(days=58)),
            ])

        if not EntregaEPP.query.first():
            db.session.add_all([
                EntregaEPP(trabajador_id=trabajador.id, elemento='Casco de seguridad',
                           referencia='3M H-700', certificacion='ANSI Z89.1',
                           fecha_entrega=hoy - timedelta(days=400), vida_util_meses=12,
                           fecha_reposicion=hoy - timedelta(days=40), capacitado_en_uso=True,
                           constancia='Acta 014', entregado_por_id=admin.id),
                EntregaEPP(trabajador_id=trabajador.id, elemento='Botas de seguridad',
                           certificacion='NTC 2396', fecha_entrega=hoy - timedelta(days=90),
                           vida_util_meses=12, fecha_reposicion=hoy + timedelta(days=275),
                           capacitado_en_uso=False, entregado_por_id=admin.id),
            ])

        if not CondicionInsegura.query.first():
            rep = CondicionInsegura(titulo='Escalera sin baranda en bodega 2',
                                    descripcion='Acceso al mezzanine sin baranda ni línea de vida.',
                                    ubicacion='Bodega 2', empleado_reportador_id=trabajador.id,
                                    estado='Abierto')
            rep.generar_numero_reporte()
            db.session.add(rep)

        if not RiesgoMatriz.query.first():
            riesgo = RiesgoMatriz(nombre_riesgo='Caída a distinto nivel en mezzanine',
                                  probabilidad=3, severidad=4)
            riesgo.calcular_clasificacion()
            db.session.add(riesgo)
            db.session.flush()
            db.session.add(Control(codigo='CTL-001-2026', nombre='Instalar baranda y línea de vida',
                                   riesgo_id=riesgo.id, responsable_id=admin.id,
                                   creado_por=admin.id, requiere_seguimiento_periodico=True,
                                   frecuencia_seguimiento_dias=30,
                                   proximo_seguimiento=datetime.utcnow() + timedelta(days=25)))

        if not ConsultaJuridica.query.first():
            con = ConsultaJuridica(titulo='Reporte extemporáneo de accidente leve',
                                   descripcion='Un AT leve se reportó a la ARL al cuarto día hábil.',
                                   tipo_consulta='Laboral', responsable_creador_id=admin.id,
                                   prioridad='Alta', riesgo_legal='Alto')
            con.generar_numero_consulta()
            db.session.add(con)

        if not Curso.query.first():
            curso = Curso(titulo='Inducción en SST', descripcion='Curso de ingreso.',
                          categoria='Inducción', tipo_contenido='pdf', duracion_horas=2)
            db.session.add(curso)
            db.session.flush()
            ex = Examen(curso_id=curso.id, titulo='Examen de inducción', porcentaje_aprobacion=70)
            db.session.add(ex)
            db.session.flush()
            p = Pregunta(examen_id=ex.id, texto_pregunta='¿Qué norma regula el SG-SST?', puntaje=10)
            db.session.add(p)
            db.session.flush()
            db.session.add_all([Opcion(pregunta_id=p.id, texto_opcion='Decreto 1072 de 2015', es_correcta=True),
                                Opcion(pregunta_id=p.id, texto_opcion='Ley 100 de 1993')])

        db.session.commit()

        # Cumplimiento: SARLAFT simplificado y datos personales con contrapartes
        from app.models.cumplimiento import ProgramaCumplimiento, Contraparte, RiesgoCumplimiento
        from app.services import cumplimiento_service as csvc
        if not ProgramaCumplimiento.query.first():
            sarlaft = csvc.activar_programa('sarlaft_transporte', 'simplificado', admin.id)
            csvc.activar_programa('datos_personales', 'documental', admin.id)
            sarlaft.oficial_nombre, sarlaft.oficial_tipo = 'Marta Díaz', 'externo'
            for r in sarlaft.requisitos:
                if r.codigo in ('politica', 'oficial'):
                    csvc.marcar_requisito(r, 'cumplido', evidencia='Acta 12 de junta de socios',
                                          fecha=hoy - timedelta(days=30))
                elif r.codigo == 'capacitacion':
                    csvc.marcar_requisito(r, 'cumplido', evidencia='Curso UIAF, 18 asistentes',
                                          fecha=hoy - timedelta(days=400))   # revisión vencida
            db.session.add_all([
                RiesgoCumplimiento(programa=sarlaft, factor='canal', probabilidad=4, impacto=4,
                                   descripcion='Pagos de fletes en efectivo por terceros distintos del cliente',
                                   controles='Solo transferencia desde cuenta del cliente', probabilidad_residual=2, impacto_residual=4),
                RiesgoCumplimiento(programa=sarlaft, factor='contraparte', probabilidad=3, impacto=5,
                                   descripcion='Propietarios de vehículos afiliados sin verificación en listas'),
                Contraparte(nombre='Agroexportadora del Llano S.A.S.', tipo='cliente', documento='900222333',
                            nivel_riesgo='medio', ultima_verificacion=hoy - timedelta(days=20),
                            resultado_verificacion='sin_coincidencia', fuente_verificacion='ONU y OFAC (manual)',
                            proxima_verificacion=hoy + timedelta(days=345), creado_por_id=admin.id),
                Contraparte(nombre='Pedro Antonio Lara', tipo='propietario_vehiculo', tipo_documento='CC',
                            documento='79456123', nivel_riesgo='bajo', creado_por_id=admin.id),
                Contraparte(nombre='Combustibles La Y Ltda.', tipo='proveedor', documento='830111222',
                            nivel_riesgo='alto', pep=False, ultima_verificacion=hoy - timedelta(days=200),
                            resultado_verificacion='sin_coincidencia', fuente_verificacion='OFAC (manual)',
                            proxima_verificacion=hoy - timedelta(days=18), creado_por_id=admin.id),
            ])
            db.session.commit()

        from scripts.seed_matriz_legal import seed
        seed()
        set_empresa(None)
        print('seed_demo: OK (admin@sst.local / admin123)')


if __name__ == '__main__':
    os.environ.setdefault('SCHEDULER_ENABLED', '0')
    main()
