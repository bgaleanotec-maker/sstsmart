"""
Script para cargar datos iniciales en la base de datos
Uso: python scripts/seed_data.py
"""
import sys
import os

# Agregar la ruta del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import (
    CategoriaArea, Dependencia, RolSST, TipoReporte, 
    TipoEvidencia, MetodologiaInvestigacion
)

def seed_all():
    """Carga todos los datos iniciales"""
    app = create_app()
    with app.app_context():
        print("🌱 Iniciando carga de datos...")
        
        # 1. Categorías de Áreas
        print("  📁 Creando categorías...")
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
        print("  ✅ Categorías creadas")
        
        # 2. Roles SST
        print("  👥 Creando roles...")
        roles_data = [
            {
                'nombre': 'Empleado',
                'descripcion': 'Empleado regular que puede reportar',
                'permisos': ['reportar', 'ver_propios_reportes']
            },
            {
                'nombre': 'Responsable_SST',
                'descripcion': 'Responsable de Seguridad y Salud en el Trabajo',
                'permisos': ['reportar', 'investigar', 'autorizar', 'ver_todos_reportes']
            },
            {
                'nombre': 'Gerente',
                'descripcion': 'Gerente de la empresa',
                'permisos': ['reportar', 'ver_todos_reportes', 'ver_estadisticas']
            },
            {
                'nombre': 'Abogado',
                'descripcion': 'Asesor legal',
                'permisos': ['ver_consultas_juridicas', 'crear_consultas']
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
        print("  ✅ Roles creados")
        
        # 3. Dependencias
        print("  🏢 Creando dependencias...")
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
            },
            {
                'nombre': 'Almacén Central',
                'descripcion': 'Almacén centralizado',
                'direccion': 'Calle 22 #68-90, Bogotá',
                'latitud': 4.7080,
                'longitud': -74.0890,
                'categoria': 'Almacén'
            },
            {
                'nombre': 'Centro de Distribución',
                'descripcion': 'Centro de distribución y logística',
                'direccion': 'Calle 40 norte #1-50, Bogotá',
                'latitud': 4.7450,
                'longitud': -74.0650,
                'categoria': 'Logística'
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
                    # Vincular todos los roles
                    for role in RolSST.query.all():
                        dep.roles_vinculados.append(role)
                    db.session.add(dep)
        
        db.session.commit()
        print("  ✅ Dependencias creadas")
        
        # 4. Tipos de Reporte
        print("  📋 Creando tipos de reporte...")
        tipos_reporte_data = [
            {
                'nombre': 'Incidente de trabajo',
                'descripcion': 'Suceso acaecido en el curso del trabajo',
                'requiere_investigacion': True
            },
            {
                'nombre': 'Acto inseguro',
                'descripcion': 'Acción contraria a los procedimientos de seguridad',
                'requiere_investigacion': True
            },
            {
                'nombre': 'Condición insegura',
                'descripcion': 'Condición peligrosa en el ambiente de trabajo',
                'requiere_investigacion': True
            },
            {
                'nombre': 'Casi accidente',
                'descripcion': 'Evento que pudo haber causado daño',
                'requiere_investigacion': False
            }
        ]
        
        for tipo_data in tipos_reporte_data:
            existing = TipoReporte.query.filter_by(nombre=tipo_data['nombre']).first()
            if not existing:
                tipo = TipoReporte(**tipo_data)
                db.session.add(tipo)
        
        db.session.commit()
        print("  ✅ Tipos de reporte creados")
        
        # 5. Tipos de Evidencia
        print("  👁️ Creando tipos de evidencia...")
        tipos_evidencia_data = [
            {
                'nombre': 'Acto Inseguro (RIESGO)',
                'codigo': 'ACTO_INSEGURO_RIESGO',
                'descripcion': 'Acción que genera riesgo'
            },
            {
                'nombre': 'Condición Insegura (RIESGO)',
                'codigo': 'CONDICION_INSEGURA_RIESGO',
                'descripcion': 'Condición que genera riesgo'
            },
            {
                'nombre': 'Acto Seguro (OPORTUNIDAD DE MEJORA)',
                'codigo': 'ACTO_SEGURO_MEJORA',
                'descripcion': 'Acción segura que es ejemplo'
            },
            {
                'nombre': 'Condición Segura (OPORTUNIDAD DE MEJORA)',
                'codigo': 'CONDICION_SEGURA_MEJORA',
                'descripcion': 'Condición segura que es ejemplo'
            }
        ]
        
        for tipo_data in tipos_evidencia_data:
            existing = TipoEvidencia.query.filter_by(nombre=tipo_data['nombre']).first()
            if not existing:
                tipo = TipoEvidencia(**tipo_data)
                db.session.add(tipo)
        
        db.session.commit()
        print("  ✅ Tipos de evidencia creados")
        
        # 6. Metodologías de Investigación
        print("  📚 Creando metodologías...")
        metodologias_data = [
            {
                'nombre': 'Espina de Pescado (Ishikawa)',
                'descripcion': 'Análisis de causas usando 6 categorías: Mano de obra, Materiales, Métodos, Máquinas, Medioambiente, Medición'
            },
            {
                'nombre': 'Cinco Porqués',
                'descripcion': 'Análisis iterativo preguntando "¿Por qué?" hasta 5 veces para encontrar la causa raíz'
            },
            {
                'nombre': 'Árbol de Causas',
                'descripcion': 'Representación gráfica de causas en forma de árbol'
            },
            {
                'nombre': 'Diagrama de Flujo',
                'descripcion': 'Análisis del proceso paso a paso'
            },
            {
                'nombre': 'Análisis de Factores Humanos',
                'descripcion': 'Enfoque en errores humanos y comportamientos'
            }
        ]
        
        for met_data in metodologias_data:
            existing = MetodologiaInvestigacion.query.filter_by(nombre=met_data['nombre']).first()
            if not existing:
                met = MetodologiaInvestigacion(**met_data)
                db.session.add(met)
        
        db.session.commit()
        print("  ✅ Metodologías creadas")
        
        print("\n" + "="*50)
        print("✅ 🌱 ¡Datos iniciales cargados exitosamente!")
        print("="*50)
        print("\nResumen:")
        print(f"  - Categorías: {CategoriaArea.query.count()}")
        print(f"  - Dependencias: {Dependencia.query.count()}")
        print(f"  - Roles: {RolSST.query.count()}")
        print(f"  - Tipos de Reporte: {TipoReporte.query.count()}")
        print(f"  - Tipos de Evidencia: {TipoEvidencia.query.count()}")
        print(f"  - Metodologías: {MetodologiaInvestigacion.query.count()}")
        print("="*50)

if __name__ == '__main__':
    try:
        seed_all()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()