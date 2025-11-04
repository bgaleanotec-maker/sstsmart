#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script completo de inicialización del módulo jurídico
Ejecuta todos los pasos necesarios para dejar el módulo listo
Uso: python scripts/inicializar_modulo_juridico.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import (
    TablaRetencion, TablasRetencionPredefinidas, 
    Usuario, Abogado
)

def banner():
    """Muestra banner de bienvenida"""
    print("\n" + "=" * 70)
    print("  🛡️  INICIALIZACIÓN DEL MÓDULO JURÍDICO - SST SMART")
    print("=" * 70 + "\n")

def paso_1_tabla_retencion(app):
    """Paso 1: Crear tabla de retención"""
    with app.app_context():
        print("📋 PASO 1: Creando Tabla de Retención Documental")
        print("-" * 70)
        
        existentes = TablaRetencion.query.count()
        
        if existentes > 0:
            print(f"⚠️  Ya existen {existentes} registros")
            return True
        
        try:
            for tabla_data in TablasRetencionPredefinidas.PREDEFINIDAS:
                tabla = TablaRetencion(
                    codigo=tabla_data['codigo'],
                    tipo_documento=tabla_data['tipo_documento'],
                    tiempo_retencion_anos=tabla_data['tiempo_retencion_anos'],
                    disposicion_final=tabla_data['disposicion_final'],
                    normativa_aplicable=tabla_data['normativa_aplicable'],
                    activa=True
                )
                db.session.add(tabla)
                print(f"  ✓ {tabla_data['codigo']} - {tabla_data['tipo_documento']} ({tabla_data['tiempo_retencion_anos']} años)")
            
            db.session.commit()
            print(f"\n✅ Tabla de retención creada: {TablaRetencion.query.count()} registros\n")
            return True
        
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {str(e)}\n")
            return False

def paso_2_crear_carpetas(app):
    """Paso 2: Crear carpetas necesarias"""
    print("📁 PASO 2: Creando Estructura de Carpetas")
    print("-" * 70)
    
    carpetas = [
        'uploads/documentos_juridicos',
        'logs',
        'backups'
    ]
    
    for carpeta in carpetas:
        try:
            os.makedirs(carpeta, exist_ok=True)
            print(f"  ✓ {carpeta}/")
        except Exception as e:
            print(f"  ⚠️  Error creando {carpeta}: {str(e)}")
    
    print(f"\n✅ Carpetas creadas/verificadas\n")

def paso_3_crear_abogado_demo(app):
    """Paso 3: Crear abogado de demostración"""
    with app.app_context():
        print("👨‍⚖️ PASO 3: Creando Abogado de Demostración")
        print("-" * 70)
        
        usuario_existente = Usuario.query.filter_by(email='abogado@demo.com').first()
        
        if usuario_existente:
            print("⚠️  El usuario abogado@demo.com ya existe")
            print("  Se mantiene el usuario existente\n")
            return True
        
        try:
            usuario = Usuario(
                email='abogado@demo.com',
                nombre_completo='Juan Carlos Méndez',
                rol='Abogado',
                activo=True
            )
            usuario.set_password('demo123456')
            
            db.session.add(usuario)
            db.session.flush()
            
            abogado = Abogado(
                usuario_id=usuario.id,
                numero_cedula='80123456789',
                numero_tarjeta_profesional='123456',
                especialidades=['Laboral', 'Civil', 'Administrativo'],
                anos_experiencia=8,
                casos_exitosos=45,
                calificacion_promedio=4.8,
                telefono='+57 300 123 4567',
                ciudad='Bogotá',
                tarifa_consulta_minuto=500,
                horas_disponibles=25,
                estado_disponibilidad='Disponible',
                horario_atencion={
                    'lunes': ['08:00', '17:00'],
                    'martes': ['08:00', '17:00'],
                    'miercoles': ['08:00', '17:00'],
                    'jueves': ['08:00', '17:00'],
                    'viernes': ['08:00', '17:00']
                }
            )
            
            db.session.add(abogado)
            db.session.commit()
            
            print(f"  ✓ Usuario: {usuario.email}")
            print(f"  ✓ Nombre: {abogado.usuario.nombre_completo}")
            print(f"  ✓ Especialidades: {', '.join(abogado.especialidades)}")
            print(f"  ✓ Experiencia: {abogado.anos_experiencia} años")
            print(f"  ✓ Contraseña: demo123456 (⚠️ CAMBIAR EN PRODUCCIÓN)\n")
            print(f"✅ Abogado de demostración creado\n")
            return True
        
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {str(e)}\n")
            return False

def paso_4_permisos(app):
    """Paso 4: Información sobre permisos"""
    print("🔐 PASO 4: Configuración de Permisos")
    print("-" * 70)
    print("""
Los siguientes roles tienen acceso al módulo jurídico:

✓ Admin
  - Acceso completo a todas las funciones
  - Gestión de abogados
  - Auditoría completa
  - Configuración de tabla de retención

✓ Responsable_SST
  - Crear y gestionar consultas
  - Asignar abogados
  - Ver auditoría
  - Acceso a todos los documentos

✓ Abogado
  - Ver consultas asignadas
  - Emitir conceptos
  - Agregar documentos
  - Hacer comentarios

✓ Cliente/Empleado
  - Ver consultas propias
  - Descargar documentos
  - Hacer comentarios
  - Calificar abogados
""")
    print(f"\n✅ Configuración de permisos completada\n")

def paso_5_verificacion(app):
    """Paso 5: Verificación final"""
    with app.app_context():
        print("✔️ PASO 5: Verificación Final")
        print("-" * 70)
        
        tablas = TablaRetencion.query.count()
        print(f"  ✓ Tablas de retención: {tablas}")
        
        abogados = Abogado.query.count()
        print(f"  ✓ Abogados registrados: {abogados}")
        
        print(f"\n✅ Inicialización completada correctamente\n")

def mostrar_proximos_pasos():
    """Muestra los próximos pasos a seguir"""
    print("=" * 70)
    print("  📋 PRÓXIMOS PASOS")
    print("=" * 70 + "\n")
    
    print("""
1. CREAR MÁS ABOGADOS:
   - Accede a Admin → Usuarios → Crear nuevo usuario
   - Asigna rol "Abogado"
   - Crea su perfil de abogado con especialidades

2. CONFIGURAR NOTIFICACIONES:
   - Verifica que el email esté configurado correctamente
   - Prueba envío de notificaciones de test

3. CAPACITAR A USUARIOS:
   - Compartir guía de usuario
   - Realizar sesión de demostración
   - Responder preguntas

4. INICIAR OPERACIONES:
   - Crear primeras consultas jurídicas
   - Probar asignación de abogados
   - Verificar flujo completo

5. MONITOREO:
   - Revisar auditoría regularmente
   - Validar cumplimiento normativo
   - Optimizar procesos

✅ ¡El módulo jurídico está listo para usar!
""")

def main():
    """Función principal"""
    banner()
    
    app = create_app()
    
    # Ejecutar pasos
    pasos = [
        ("Tabla de Retención", paso_1_tabla_retencion),
        ("Carpetas", paso_2_crear_carpetas),
        ("Abogado Demo", paso_3_crear_abogado_demo),
        ("Permisos", paso_4_permisos),
        ("Verificación", paso_5_verificacion)
    ]
    
    completados = 0
    
    for nombre_paso, funcion_paso in pasos:
        try:
            if funcion_paso(app):
                completados += 1
            else:
                print(f"⚠️  {nombre_paso} completado con advertencias\n")
        except Exception as e:
            print(f"❌ Error en {nombre_paso}: {str(e)}\n")
    
    # Mostrar resumen
    print("=" * 70)
    print(f"  📊 RESUMEN: {completados}/{len(pasos)} pasos completados")
    print("=" * 70 + "\n")
    
    if completados == len(pasos):
        print("✅ INICIALIZACIÓN COMPLETADA EXITOSAMENTE\n")
        mostrar_proximos_pasos()
    else:
        print("⚠️  Algunos pasos tuvieron problemas. Revisa los errores anteriores.\n")
        sys.exit(1)

if __name__ == '__main__':
    main()