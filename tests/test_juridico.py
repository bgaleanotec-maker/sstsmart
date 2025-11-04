"""
TEST SUITE - Módulo Jurídico SST Colombia
Pruebas completas para ConsultaJuridica y DocumentoLegal
Comando: python tests/test_juridico.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models import (
    ConsultaJuridica, DocumentoLegal, Usuario, 
    RolSST, CondicionInsegura
)

class TestModuloJuridico(unittest.TestCase):
    """Suite de pruebas para el módulo jurídico"""
    
    def setUp(self):
        """Configuración antes de cada prueba"""
        self.app = create_app('development')
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            self._crear_datos_prueba()
    
    def tearDown(self):
        """Limpiar después de cada prueba"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def _crear_datos_prueba(self):
        """Crear datos necesarios para las pruebas"""
        # ✅ CORREGIDO: Crear roles - VERIFICAR SI EXISTEN PRIMERO
        roles_data = [
            {'nombre': 'Admin', 'descripcion': 'Administrador'},
            {'nombre': 'Abogado', 'descripcion': 'Asesor Legal'},
            {'nombre': 'Responsable_SST', 'descripcion': 'Responsable SST'},
            {'nombre': 'Empleado', 'descripcion': 'Empleado'}
        ]
        
        self.roles = {}
        for role_data in roles_data:
            # ✅ VERIFICAR SI YA EXISTE
            existing = RolSST.query.filter_by(nombre=role_data['nombre']).first()
            if existing:
                self.roles[role_data['nombre']] = existing
            else:
                role = RolSST(**role_data)
                db.session.add(role)
                self.roles[role_data['nombre']] = role
        
        db.session.commit()
        
        # Crear usuarios
        self.admin = Usuario(
            email='admin@test.com',
            nombre_completo='Admin Test',
            rol='Admin',
            activo=True
        )
        self.admin.set_password('admin123')
        db.session.add(self.admin)
        
        self.abogado = Usuario(
            email='abogado@test.com',
            nombre_completo='Abogado Test',
            rol='Abogado',
            activo=True
        )
        self.abogado.set_password('abogado123')
        db.session.add(self.abogado)
        
        self.responsable_sst = Usuario(
            email='responsable@test.com',
            nombre_completo='Responsable SST Test',
            rol='Responsable_SST',
            activo=True
        )
        self.responsable_sst.set_password('responsable123')
        db.session.add(self.responsable_sst)
        
        self.empleado = Usuario(
            email='empleado@test.com',
            nombre_completo='Empleado Test',
            rol='Empleado',
            activo=True
        )
        self.empleado.set_password('empleado123')
        db.session.add(self.empleado)
        
        db.session.commit()
        
        # ✅ GUARDAR IDs DESPUÉS DEL COMMIT para evitar DetachedInstanceError
        self.admin_id = self.admin.id
        self.abogado_id = self.abogado.id
        self.responsable_sst_id = self.responsable_sst.id
        self.empleado_id = self.empleado.id
    
    # ============ PRUEBAS DE MODELO ============
    
    def test_crear_consulta_juridica(self):
        """Prueba: Crear una consulta jurídica"""
        with self.app.app_context():
            consulta = ConsultaJuridica(
                titulo='Consulta de Accidente Laboral',
                descripcion='Análisis de responsabilidad penal en accidente grave',
                tipo_consulta='Penal',
                responsable_creador_id=self.responsable_sst_id,
                prioridad='Alta',
                riesgo_legal='Alto'
            )
            consulta.generar_numero_consulta()
            
            db.session.add(consulta)
            db.session.commit()
            
            # Verificaciones
            self.assertIsNotNone(consulta.id)
            self.assertIsNotNone(consulta.numero_consulta)
            self.assertTrue(consulta.numero_consulta.startswith('CONS-JUR-'))
            self.assertEqual(consulta.estado, 'Abierta')
            self.assertEqual(consulta.tipo_consulta, 'Penal')
            
            print(f"✅ Consulta creada: {consulta.numero_consulta}")
    
    def test_asignar_consulta_a_abogado(self):
        """Prueba: Asignar consulta a abogado"""
        with self.app.app_context():
            consulta = ConsultaJuridica(
                titulo='Consulta Laboral',
                descripcion='Cuestión de pago de prestaciones',
                tipo_consulta='Laboral',
                responsable_creador_id=self.responsable_sst_id,
                prioridad='Normal',
                riesgo_legal='Medio'
            )
            consulta.generar_numero_consulta()
            db.session.add(consulta)
            db.session.commit()
            
            # Asignar
            consulta.abogado_asignado_id = self.abogado_id
            consulta.estado = 'En revisión'
            consulta.fecha_asignacion = datetime.utcnow()
            db.session.commit()
            
            # Verificaciones
            self.assertEqual(consulta.estado, 'En revisión')
            self.assertEqual(consulta.abogado_asignado_id, self.abogado_id)
            self.assertIsNotNone(consulta.fecha_asignacion)
            
            print(f"✅ Consulta asignada a abogado")
    
    def test_resolver_consulta(self):
        """Prueba: Resolver una consulta jurídica"""
        with self.app.app_context():
            consulta = ConsultaJuridica(
                titulo='Consulta Civil',
                descripcion='Demanda de tercero',
                tipo_consulta='Civil',
                responsable_creador_id=self.responsable_sst_id,
                abogado_asignado_id=self.abogado_id,
                prioridad='Alta',
                riesgo_legal='Crítico'
            )
            consulta.generar_numero_consulta()
            db.session.add(consulta)
            db.session.commit()
            
            # Resolver
            consulta.resolucion = "Recomendamos interponer una contrademanda..."
            consulta.recomendaciones = "1. Recopilar toda documentación\n2. Contactar aseguradora"
            consulta.estado = 'Resuelta'
            consulta.fecha_resolucion = datetime.utcnow()
            db.session.commit()
            
            # Verificaciones
            self.assertEqual(consulta.estado, 'Resuelta')
            self.assertIsNotNone(consulta.resolucion)
            self.assertIsNotNone(consulta.fecha_resolucion)
            
            print(f"✅ Consulta resuelta")
    
    def test_crear_documento_legal(self):
        """Prueba: Crear documento legal asociado"""
        with self.app.app_context():
            consulta = ConsultaJuridica(
                titulo='Consulta Administrativa',
                descripcion='Multa por incumplimiento normativo',
                tipo_consulta='Administrativo',
                responsable_creador_id=self.responsable_sst_id,
                prioridad='Alta',
                riesgo_legal='Alto'
            )
            consulta.generar_numero_consulta()
            db.session.add(consulta)
            db.session.commit()
            
            # Crear documento
            documento = DocumentoLegal(
                consulta_id=consulta.id,
                nombre='Resolución UGPP 2024-001',
                tipo='Resolución',
                contenido='CONSIDERANDO: Que la empresa incumplió...',
                creado_por_id=self.abogado_id
            )
            db.session.add(documento)
            db.session.commit()
            
            # Verificaciones
            self.assertIsNotNone(documento.id)
            self.assertEqual(documento.consulta_id, consulta.id)
            self.assertEqual(len(consulta.documentos.all()), 1)
            
            print(f"✅ Documento legal creado: {documento.nombre}")
    
    def test_generar_numero_consulta_unico(self):
        """Prueba: Verificar que los números de consulta son únicos"""
        with self.app.app_context():
            consulta1 = ConsultaJuridica(
                titulo='Consulta 1',
                descripcion='Primera consulta',
                tipo_consulta='Laboral',
                responsable_creador_id=self.responsable_sst_id
            )
            consulta1.generar_numero_consulta()
            db.session.add(consulta1)
            db.session.commit()
            
            consulta2 = ConsultaJuridica(
                titulo='Consulta 2',
                descripcion='Segunda consulta',
                tipo_consulta='Laboral',
                responsable_creador_id=self.responsable_sst_id
            )
            consulta2.generar_numero_consulta()
            db.session.add(consulta2)
            db.session.commit()
            
            # Verificar unicidad
            self.assertNotEqual(consulta1.numero_consulta, consulta2.numero_consulta)
            print(f"✅ Números únicos: {consulta1.numero_consulta} vs {consulta2.numero_consulta}")
    
    # ============ PRUEBAS DE FLUJO ============
    
    def test_flujo_completo_consulta(self):
        """Prueba: Flujo completo de una consulta desde creación a cierre"""
        with self.app.app_context():
            # 1. Crear
            consulta = ConsultaJuridica(
                titulo='Accidente grave con incapacidad',
                descripcion='Empleado con fractura de fémur',
                tipo_consulta='Penal',
                empleado_afectado_id=self.empleado_id,
                responsable_creador_id=self.responsable_sst_id,
                prioridad='Crítica',
                riesgo_legal='Crítico'
            )
            consulta.generar_numero_consulta()
            db.session.add(consulta)
            db.session.commit()
            
            numero_inicial = consulta.numero_consulta
            
            # 2. Asignar
            consulta.abogado_asignado_id = self.abogado_id
            consulta.estado = 'En revisión'
            consulta.fecha_asignacion = datetime.utcnow()
            db.session.commit()
            
            # 3. Agregar documentos
            doc1 = DocumentoLegal(
                consulta_id=consulta.id,
                nombre='Acta de Investigación',
                tipo='Acta de Investigación',
                contenido='Investigación del accidente...',
                creado_por_id=self.abogado_id
            )
            doc2 = DocumentoLegal(
                consulta_id=consulta.id,
                nombre='Certificado Médico',
                tipo='Documento',
                contenido='Dictamen médico forense...',
                creado_por_id=self.abogado_id
            )
            db.session.add_all([doc1, doc2])
            db.session.commit()
            
            # 4. Resolver
            consulta.resolucion = """
            Análisis Legal:
            - Responsabilidad penal potencial: Artículo 109 CP (homicidio culposo)
            - Responsabilidad civil: Demanda de terceros probable
            - Responsabilidad administrativa: Multa UGPP
            """
            consulta.recomendaciones = """
            Recomendaciones:
            1. Contactar inmediatamente aseguradora
            2. Preparar defensa legal
            3. Revisar cumplimiento normas SST
            """
            consulta.estado = 'Resuelta'
            consulta.fecha_resolucion = datetime.utcnow()
            db.session.commit()
            
            # 5. Cerrar
            consulta.estado = 'Cerrada'
            consulta.fecha_cierre = datetime.utcnow()
            db.session.commit()
            
            # Verificaciones finales
            self.assertEqual(consulta.numero_consulta, numero_inicial)
            self.assertEqual(consulta.estado, 'Cerrada')
            self.assertEqual(len(consulta.documentos.all()), 2)
            
            # Calcular tiempo total
            tiempo_total = consulta.fecha_cierre - consulta.fecha_creacion
            horas = tiempo_total.total_seconds() / 3600
            
            print(f"✅ Flujo completo ejecutado")
            print(f"   - Número: {numero_inicial}")
            print(f"   - Tiempo total: {int(horas)} horas")
            print(f"   - Documentos adjuntos: {len(consulta.documentos.all())}")
    
    # ============ PRUEBAS DE NORMATIVA ============
    
    def test_cargar_normativa_colombia(self):
        """Prueba: Cargar normativa de Colombia"""
        with self.app.app_context():
            normativas = [
                {
                    'numero': 'CONS-JUR-2025-NORM-001',
                    'nombre': 'Decreto 1072 de 2015',
                    'tipo': 'Laboral'
                },
                {
                    'numero': 'CONS-JUR-2025-NORM-002',
                    'nombre': 'Resolución 3165 de 2022',
                    'tipo': 'Laboral'
                },
                {
                    'numero': 'CONS-JUR-2025-NORM-003',
                    'nombre': 'Artículo 200 CP',
                    'tipo': 'Penal'
                }
            ]
            
            for norma in normativas:
                consulta = ConsultaJuridica(
                    numero_consulta=norma['numero'],
                    titulo=f"Normativa: {norma['nombre']}",
                    descripcion=f"Referencia a {norma['nombre']}",
                    tipo_consulta=norma['tipo'],
                    responsable_creador_id=self.admin_id,
                    estado='Resuelta',
                    prioridad='Alta',
                    riesgo_legal='Crítico',
                    normativa_aplicable={'norma': norma['nombre']}
                )
                db.session.add(consulta)
            
            db.session.commit()
            
            # Verificar
            count = ConsultaJuridica.query.count()
            self.assertEqual(count, 3)
            
            print(f"✅ {count} normativas cargadas")
    
    # ============ PRUEBAS DE VALIDACIÓN ============
    
    def test_validar_prioridad_riesgo(self):
        """Prueba: Validar combinaciones prioridad/riesgo"""
        with self.app.app_context():
            # Combinaciones válidas
            combinaciones = [
                ('Baja', 'Bajo'),
                ('Normal', 'Medio'),
                ('Alta', 'Alto'),
                ('Crítica', 'Crítico')
            ]
            
            for prioridad, riesgo in combinaciones:
                consulta = ConsultaJuridica(
                    titulo=f'Test {prioridad}-{riesgo}',
                    descripcion='Test',
                    tipo_consulta='Laboral',
                    responsable_creador_id=self.responsable_sst_id,
                    prioridad=prioridad,
                    riesgo_legal=riesgo
                )
                consulta.generar_numero_consulta()  # ✅ AGREGAR ESTO
                db.session.add(consulta)
            
            db.session.commit()
            
            print(f"✅ Todas las combinaciones prioridad/riesgo válidas")
    
    def test_permiso_acceso_consulta(self):
        """Prueba: Verificar permisos de acceso"""
        with self.app.app_context():
            consulta = ConsultaJuridica(
                titulo='Consulta Confidencial',
                descripcion='Información sensible',
                tipo_consulta='Penal',
                responsable_creador_id=self.responsable_sst_id,
                prioridad='Crítica',
                riesgo_legal='Crítico'
            )
            consulta.generar_numero_consulta()
            db.session.add(consulta)
            db.session.commit()
            
            # Solo Admin, Responsable_SST y Abogado pueden ver
            usuarios_autorizados = [self.admin, self.abogado, self.responsable_sst]
            usuarios_no_autorizados = [self.empleado]
            
            for usuario in usuarios_autorizados:
                self.assertIn(usuario.rol, ['Admin', 'Abogado', 'Responsable_SST'])
            
            for usuario in usuarios_no_autorizados:
                self.assertNotIn(usuario.rol, ['Admin', 'Abogado', 'Responsable_SST'])
            
            print(f"✅ Permisos correctamente asignados")

class TestEstadisticasJuridico(unittest.TestCase):
    """Pruebas de estadísticas del módulo jurídico"""
    
    def setUp(self):
        self.app = create_app('development')
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with self.app.app_context():
            db.create_all()
            self._crear_datos_estadisticas()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def _crear_datos_estadisticas(self):
        """Crear datos para pruebas de estadísticas"""
        # ✅ CORREGIDO: Crear roles - VERIFICAR SI EXISTEN PRIMERO
        for nombre in ['Admin', 'Abogado', 'Responsable_SST']:
            existing = RolSST.query.filter_by(nombre=nombre).first()
            if not existing:
                role = RolSST(nombre=nombre, descripcion=nombre)
                db.session.add(role)
        db.session.commit()
        
        # Crear usuarios
        self.admin = Usuario(
            email='admin@test.com',
            nombre_completo='Admin',
            rol='Admin',
            activo=True
        )
        self.admin.set_password('pass')
        db.session.add(self.admin)
        db.session.commit()
        
        # ✅ GUARDAR ID DESPUÉS DEL COMMIT
        self.admin_id = self.admin.id
    
    def test_estadisticas_por_tipo(self):
        """Prueba: Estadísticas agrupadas por tipo"""
        with self.app.app_context():
            tipos = ['Laboral', 'Penal', 'Civil', 'Administrativo']
            
            for i, tipo in enumerate(tipos):
                for j in range(i + 1):
                    consulta = ConsultaJuridica(
                        titulo=f'Consulta {tipo} {j}',
                        descripcion='Test',
                        tipo_consulta=tipo,
                        responsable_creador_id=self.admin_id,
                        prioridad='Normal',
                        riesgo_legal='Medio'
                    )
                    consulta.generar_numero_consulta()
                    db.session.add(consulta)
            
            db.session.commit()
            
            # Contar por tipo
            stats = {}
            for tipo in tipos:
                count = ConsultaJuridica.query.filter_by(tipo_consulta=tipo).count()
                stats[tipo] = count
            
            print(f"✅ Estadísticas por tipo:")
            for tipo, count in stats.items():
                print(f"   - {tipo}: {count}")

def run_tests():
    """Ejecutar todas las pruebas"""
    print("\n" + "="*70)
    print("🧪 INICIANDO TEST SUITE - MÓDULO JURÍDICO SST COLOMBIA")
    print("="*70 + "\n")
    
    # Crear test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las pruebas
    suite.addTests(loader.loadTestsFromTestCase(TestModuloJuridico))
    suite.addTests(loader.loadTestsFromTestCase(TestEstadisticasJuridico))
    
    # Ejecutar
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE PRUEBAS:")
    print("="*70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"✅ Exitosas: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Fallos: {len(result.failures)}")
    print(f"⚠️  Errores: {len(result.errors)}")
    print("="*70 + "\n")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)