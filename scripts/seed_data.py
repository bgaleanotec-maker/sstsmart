"""
Script para cargar datos iniciales en la base de datos - CON MÓDULO JURÍDICO CORREGIDO
Uso: python scripts/seed_data.py
Enfoque: Cumplimiento normativo SST Colombia 2025
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import (
    CategoriaArea, Dependencia, RolSST, TipoReporte, 
    TipoEvidencia, MetodologiaInvestigacion,
    ConsultaJuridica, DocumentoLegal, Usuario
)
from datetime import datetime

# ============ DATOS JURÍDICOS COLOMBIA 2025 ============
NORMATIVA_COLOMBIA = {
    'Laboral': [
        {
            'codigo': 'DEC-1072-2015',
            'nombre': 'Decreto 1072 de 2015',
            'descripcion': 'Decreto Único Reglamentario del Sector Trabajo. Reglamenta todas las actividades de SST en Colombia',
            'fecha_vigencia': '2015-05-26',
            'aplicabilidad': 'Obligatoria para todas las empresas',
            'url': 'https://www.mintrabajo.gov.co'
        },
        {
            'codigo': 'RES-3165-2022',
            'nombre': 'Resolución 3165 de 2022',
            'descripcion': 'Estándares Mínimos del Sistema de Gestión SST para empleadores y contratantes',
            'fecha_vigencia': '2022-08-10',
            'aplicabilidad': 'Obligatoria para verificación de cumplimiento',
            'url': 'https://www.mintrabajo.gov.co'
        },
        {
            'codigo': 'RES-1401-2023',
            'nombre': 'Resolución 1401 de 2023',
            'descripcion': 'Accidentes de trabajo y enfermedades laborales. Investigación y registro',
            'fecha_vigencia': '2023-05-23',
            'aplicabilidad': 'Obligatoria para reporte de incidentes',
            'url': 'https://www.mintrabajo.gov.co'
        }
    ],
    'Penal': [
        {
            'codigo': 'ART-200-CP',
            'nombre': 'Artículo 200 - Código Penal',
            'descripcion': 'Lesiones culposas por incumplimiento de normas SST',
            'fecha_vigencia': '2000-01-01',
            'aplicabilidad': 'Responsabilidad penal del empleador',
            'url': 'https://www.rama-judicial.gov.co'
        },
        {
            'codigo': 'ART-109-CP',
            'nombre': 'Artículo 109 - Código Penal',
            'descripcion': 'Homicidio culposo por negligencia en SST',
            'fecha_vigencia': '2000-01-01',
            'aplicabilidad': 'Responsabilidad penal grave',
            'url': 'https://www.rama-judicial.gov.co'
        }
    ],
    'Civil': [
        {
            'codigo': 'RES-052-2012',
            'nombre': 'Resolución 052 de 2012',
            'descripcion': 'Conformación del Comité Paritario de SST (COPASOS)',
            'fecha_vigencia': '2012-01-20',
            'aplicabilidad': 'Obligatoria para empresas con más de 10 trabajadores',
            'url': 'https://www.mintrabajo.gov.co'
        }
    ],
    'Administrativo': [
        {
            'codigo': 'RES-312-2019',
            'nombre': 'Resolución 312 de 2019',
            'descripcion': 'Estándares mínimos del SGSSST para MiPymes',
            'fecha_vigencia': '2019-02-13',
            'aplicabilidad': 'Obligatoria para MiPymes',
            'url': 'https://www.mintrabajo.gov.co'
        },
        {
            'codigo': 'RES-0489-2016',
            'nombre': 'Resolución 0489 de 2016',
            'descripcion': 'Actos, procesos y procedimientos de inspección, vigilancia y control',
            'fecha_vigencia': '2016-02-17',
            'aplicabilidad': 'Para inspecciones por autoridades',
            'url': 'https://www.mintrabajo.gov.co'
        }
    ]
}

def seed_all():
    """Carga todos los datos iniciales"""
    app = create_app()
    with app.app_context():
        print("🌱 INICIANDO CARGA DE DATOS SST COLOMBIA 2025")
        print("="*60)
        
        try:
            # ========== DATOS BÁSICOS ==========
            print("\n📁 FASE 1: Categorías...")
            categorias_data = [
                {
                    'nombre': 'Industrial',
                    'descripcion': 'Áreas de producción e industrial',
                    'icono': '🏭',
                    'color': '#ef4444'
                },
                {
                    'nombre': 'Mantenimiento',
                    'descripcion': 'Áreas de mantenimiento y taller',
                    'icono': '🔧',
                    'color': '#f97316'
                },
                {
                    'nombre': 'Oficina',
                    'descripcion': 'Oficinas administrativas',
                    'icono': '🏢',
                    'color': '#3b82f6'
                },
                {
                    'nombre': 'Almacén',
                    'descripcion': 'Áreas de almacenamiento',
                    'icono': '📦',
                    'color': '#8b5cf6'
                },
                {
                    'nombre': 'Logística',
                    'descripcion': 'Transporte y distribución',
                    'icono': '🚚',
                    'color': '#06b6d4'
                }
            ]
            
            categorias = {}
            for cat_data in categorias_data:
                existing = CategoriaArea.query.filter_by(nombre=cat_data['nombre']).first()
                if not existing:
                    cat = CategoriaArea(**cat_data)
                    db.session.add(cat)
                    categorias[cat_data['nombre']] = cat
                else:
                    categorias[cat_data['nombre']] = existing
            
            db.session.commit()
            print(f"  ✅ {len(categorias)} categorías creadas/existentes")
            
            # ========== ROLES ==========
            print("\n👥 FASE 2: Roles SST...")
            roles_data = [
                {
                    'nombre': 'Empleado',
                    'descripcion': 'Empleado regular que puede reportar condiciones inseguras',
                    'permisos': ['reportar', 'ver_propios_reportes']
                },
                {
                    'nombre': 'Responsable_SST',
                    'descripcion': 'Responsable de Seguridad y Salud en el Trabajo',
                    'permisos': ['reportar', 'investigar', 'autorizar', 'ver_todos_reportes', 'crear_consultas_juridicas']
                },
                {
                    'nombre': 'Gerente',
                    'descripcion': 'Gerente de la empresa',
                    'permisos': ['reportar', 'ver_todos_reportes', 'ver_estadisticas', 'consultar_juridico']
                },
                {
                    'nombre': 'Abogado',
                    'descripcion': 'Asesor legal - Experto jurídico',
                    'permisos': ['ver_consultas_juridicas', 'crear_consultas', 'resolver_consultas', 'crear_documentos_legales']
                },
                {
                    'nombre': 'Admin',
                    'descripcion': 'Administrador del sistema',
                    'permisos': ['*']
                }
            ]
            
            roles = {}
            for role_data in roles_data:
                existing = RolSST.query.filter_by(nombre=role_data['nombre']).first()
                if not existing:
                    role = RolSST(**role_data)
                    db.session.add(role)
                    roles[role_data['nombre']] = role
                else:
                    roles[role_data['nombre']] = existing
            
            db.session.commit()
            print(f"  ✅ {len(roles)} roles creados/existentes")
            
            # ========== DEPENDENCIAS ==========
            print("\n🏢 FASE 3: Dependencias...")
            dependencias_data = [
                {
                    'nombre': 'Planta Principal',
                    'descripcion': 'Planta de producción principal',
                    'direccion': 'Calle 15 #45-67, Bogotá',
                    'latitud': 4.7110,
                    'longitud': -74.0721,
                    'categoria': 'Industrial'
                },
                {
                    'nombre': 'Oficina Administrativa',
                    'descripcion': 'Oficinas centrales administrativas',
                    'direccion': 'Carrera 7 #156-20, Bogotá',
                    'latitud': 4.7250,
                    'longitud': -74.0425,
                    'categoria': 'Oficina'
                },
                {
                    'nombre': 'Centro de Mantenimiento',
                    'descripcion': 'Centro de mantenimiento y reparación',
                    'direccion': 'Autopista sur km 3, Bogotá',
                    'latitud': 4.6950,
                    'longitud': -74.0580,
                    'categoria': 'Mantenimiento'
                }
            ]
            
            for dep_data in dependencias_data:
                existing = Dependencia.query.filter_by(nombre=dep_data['nombre']).first()
                if not existing:
                    categoria = CategoriaArea.query.filter_by(nombre=dep_data['categoria']).first()
                    if categoria:
                        dep = Dependencia(
                            nombre=dep_data['nombre'],
                            descripcion=dep_data['descripcion'],
                            direccion=dep_data['direccion'],
                            latitud=dep_data['latitud'],
                            longitud=dep_data['longitud'],
                            categoria_id=categoria.id
                        )
                        for role in RolSST.query.all():
                            dep.roles_vinculados.append(role)
                        db.session.add(dep)
            
            db.session.commit()
            print(f"  ✅ Dependencias creadas/existentes")
            
            # ========== TIPOS DE REPORTE ==========
            print("\n📋 FASE 4: Tipos de Reporte...")
            tipos_reporte_data = [
                {
                    'nombre': 'Condición Insegura',
                    'descripcion': 'Condición insegura sin accidente',
                    'requiere_investigacion': True
                },
                {
                    'nombre': 'Incidente',
                    'descripcion': 'Evento sin lesión pero que pudo causarla',
                    'requiere_investigacion': True
                },
                {
                    'nombre': 'Accidente Leve',
                    'descripcion': 'Lesión que no genera incapacidad temporal',
                    'requiere_investigacion': True
                },
                {
                    'nombre': 'Accidente Grave',
                    'descripcion': 'Lesión con incapacidad temporal mayor a 3 días',
                    'requiere_investigacion': True
                }
            ]
            
            for tipo_data in tipos_reporte_data:
                existing = TipoReporte.query.filter_by(nombre=tipo_data['nombre']).first()
                if not existing:
                    tipo = TipoReporte(**tipo_data)
                    db.session.add(tipo)
            
            db.session.commit()
            print(f"  ✅ Tipos de reporte creados/existentes")
            
            # ========== TIPOS DE EVIDENCIA ==========
            print("\n🔍 FASE 5: Tipos de Evidencia...")
            tipos_evidencia_data = [
                'Fotografía',
                'Video',
                'Testigo Presencial',
                'Documento Oficial',
                'Inspección del Área',
                'Prueba Científica',
                'Grabación de Audio'
            ]
            
            for tipo in tipos_evidencia_data:
                existing = TipoEvidencia.query.filter_by(nombre=tipo).first()
                if not existing:
                    te = TipoEvidencia(nombre=tipo)
                    db.session.add(te)
            
            db.session.commit()
            print(f"  ✅ Tipos de evidencia creados/existentes")
            
            # ========== METODOLOGÍAS ==========
            print("\n📚 FASE 6: Metodologías de Investigación...")
            metodologias_data = [
                {
                    'nombre': 'Espina de Pescado (Ishikawa)',
                    'descripcion': 'Análisis de causas: Mano de obra, Materiales, Métodos, Máquinas, Medioambiente, Medición'
                },
                {
                    'nombre': 'Cinco Porqués',
                    'descripcion': 'Análisis iterativo preguntando "¿Por qué?" hasta encontrar causa raíz'
                },
                {
                    'nombre': 'Árbol de Causas',
                    'descripcion': 'Representación gráfica de causas en forma de árbol'
                }
            ]
            
            for met_data in metodologias_data:
                existing = MetodologiaInvestigacion.query.filter_by(nombre=met_data['nombre']).first()
                if not existing:
                    met = MetodologiaInvestigacion(**met_data)
                    db.session.add(met)
            
            db.session.commit()
            print(f"  ✅ Metodologías creadas/existentes")
            
            # ========== MÓDULO JURÍDICO - DATOS COLOMBIA 2025 ==========
            print("\n⚖️  FASE 7: Normativa SST Colombia 2025...")
            
            # Crear usuario abogado de prueba
            abogado_test = Usuario.query.filter_by(email='abogado@sst.local').first()
            if not abogado_test:
                abogado_test = Usuario(
                    email='abogado@sst.local',
                    nombre_completo='Abogado SST Colombia',
                    rol='Abogado',
                    activo=True
                )
                abogado_test.set_password('abogado123')
                db.session.add(abogado_test)
                db.session.commit()
                print("    ✅ Usuario Abogado de prueba creado")
            
            # Crear usuario Responsable SST
            responsable_test = Usuario.query.filter_by(email='responsable.sst@company.com').first()
            if not responsable_test:
                responsable_test = Usuario(
                    email='responsable.sst@company.com',
                    nombre_completo='Responsable SST Empresa',
                    rol='Responsable_SST',
                    activo=True
                )
                responsable_test.set_password('responsable123')
                db.session.add(responsable_test)
                db.session.commit()
                print("    ✅ Usuario Responsable SST de prueba creado")

            # Crear usuario Admin
            admin_test = Usuario.query.filter_by(email='admin@sst.local').first()
            if not admin_test:
                admin_test = Usuario(
                    email='admin@sst.local',
                    nombre_completo='Administrador Sistema',
                    rol='Admin',
                    activo=True
                )
                admin_test.set_password('admin123')
                db.session.add(admin_test)
                db.session.commit()
                print("    ✅ Usuario Admin de prueba creado")

            # Crear usuario Empleado
            empleado_test = Usuario.query.filter_by(email='empleado@sst.local').first()
            if not empleado_test:
                empleado_test = Usuario(
                    email='empleado@sst.local',
                    nombre_completo='Empleado Demo',
                    rol='Empleado',
                    activo=True
                )
                empleado_test.set_password('empleado123')
                db.session.add(empleado_test)
                db.session.commit()
                print("    ✅ Usuario Empleado de prueba creado")

            # Crear usuario Gerente
            gerente_test = Usuario.query.filter_by(email='gerente@sst.local').first()
            if not gerente_test:
                gerente_test = Usuario(
                    email='gerente@sst.local',
                    nombre_completo='Gerente General',
                    rol='Gerente',
                    activo=True
                )
                gerente_test.set_password('gerente123')
                db.session.add(gerente_test)
                db.session.commit()
                print("    ✅ Usuario Gerente de prueba creado")
            
            # Cargar normativa - CORRECCIÓN: NO crear DocumentoLegal hasta que la consulta esté guardada
            consultas_creadas = 0
            for tipo_legal, normas in NORMATIVA_COLOMBIA.items():
                for norma in normas:
                    # Crear consulta jurídica como referencia
                    existing_consulta = ConsultaJuridica.query.filter_by(
                        numero_consulta=f"NORM-{norma['codigo']}"
                    ).first()
                    
                    if not existing_consulta:
                        consulta = ConsultaJuridica(
                            numero_consulta=f"NORM-{norma['codigo']}",
                            titulo=f"Normativa: {norma['nombre']}",
                            descripcion=norma['descripcion'],
                            tipo_consulta=tipo_legal,
                            responsable_creador_id=responsable_test.id,
                            abogado_asignado_id=abogado_test.id,
                            estado='Resuelta',
                            prioridad='Alta',
                            fecha_creacion=datetime.strptime(norma['fecha_vigencia'], '%Y-%m-%d'),
                            fecha_resolucion=datetime.now(),  # ✅ CORREGIDO: usar .now() en lugar de .utcnow()
                            riesgo_legal='Crítico',
                            normativa_aplicable={
                                'codigo': norma['codigo'],
                                'nombre': norma['nombre'],
                                'fecha_vigencia': norma['fecha_vigencia'],
                                'aplicabilidad': norma['aplicabilidad'],
                                'url': norma['url']
                            }
                        )
                        db.session.add(consulta)
                        db.session.flush()  # ✅ Obtener el ID de la consulta
                        
                        # ✅ AHORA crear DocumentoLegal con el consulta_id correcto
                        doc = DocumentoLegal(
                            consulta_id=consulta.id,  # ✅ CORREGIDO: Usar el ID de la consulta
                            nombre=f"Documento: {norma['nombre']}",
                            tipo='Normativa',
                            contenido=f"{norma['nombre']}\n{norma['descripcion']}\nVigente desde: {norma['fecha_vigencia']}",
                            creado_por_id=abogado_test.id
                        )
                        db.session.add(doc)
                        consultas_creadas += 1
            
            db.session.commit()
            print(f"  ✅ {consultas_creadas} Consultas jurídicas de referencia creadas")
            
            # ========== RESUMEN FINAL ==========
            print("\n" + "="*60)
            print("✅ 🌱 ¡DATOS INICIALES CARGADOS EXITOSAMENTE!")
            print("="*60)
            print("\n📊 RESUMEN:")
            print(f"  ├─ Categorías: {CategoriaArea.query.count()}")
            print(f"  ├─ Dependencias: {Dependencia.query.count()}")
            print(f"  ├─ Roles: {RolSST.query.count()}")
            print(f"  ├─ Tipos de Reporte: {TipoReporte.query.count()}")
            print(f"  ├─ Tipos de Evidencia: {TipoEvidencia.query.count()}")
            print(f"  ├─ Metodologías: {MetodologiaInvestigacion.query.count()}")
            print(f"  └─ Consultas Jurídicas (Normativa): {ConsultaJuridica.query.count()}")
            
            print("\n👤 USUARIOS DE PRUEBA:")
            print(f"  ├─ Admin: admin@sst.local / admin123")
            print(f"  ├─ Responsable SST: responsable.sst@company.com / responsable123")
            print(f"  ├─ Abogado: abogado@sst.local / abogado123")
            print(f"  ├─ Gerente: gerente@sst.local / gerente123")
            print(f"  └─ Empleado: empleado@sst.local / empleado123")
            
            print("\n⚖️  NORMATIVA CARGADA:")
            for tipo, normas in NORMATIVA_COLOMBIA.items():
                print(f"  ├─ {tipo}: {len(normas)} normas")
            
            print("="*60 + "\n")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    success = seed_all()
    exit(0 if success else 1)