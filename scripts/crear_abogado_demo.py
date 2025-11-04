#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para crear abogado demo/test
Uso: python scripts/crear_abogado_demo.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Usuario, Abogado

def crear_abogado_demo():
    """Crea usuario y abogado de demostración"""
    app = create_app()
    
    with app.app_context():
        print("👨‍⚖️ Creando abogado de demostración...\n")
        
        # Verificar si existe
        usuario_existente = Usuario.query.filter_by(email='abogado@demo.com').first()
        
        if usuario_existente:
            print("⚠️  El usuario abogado@demo.com ya existe")
            print("¿Deseas eliminarlo y crear uno nuevo? (s/n): ", end="")
            respuesta = input().lower()
            
            if respuesta == 's':
                abogado = Abogado.query.filter_by(usuario_id=usuario_existente.id).first()
                if abogado:
                    db.session.delete(abogado)
                db.session.delete(usuario_existente)
                db.session.commit()
                print("✓ Usuario anterior eliminado\n")
            else:
                print("✓ Operación cancelada")
                return
        
        try:
            # Crear usuario
            usuario = Usuario(
                email='abogado@demo.com',
                nombre_completo='Juan Carlos Méndez',
                rol='Abogado',
                activo=True
            )
            usuario.set_password('demo123456')  # Cambiar en producción
            
            db.session.add(usuario)
            db.session.flush()
            
            print(f"✓ Usuario creado: {usuario.nombre_completo}")
            print(f"  Email: {usuario.email}")
            print(f"  Contraseña: demo123456\n")
            
            # Crear perfil de abogado
            abogado = Abogado(
                usuario_id=usuario.id,
                numero_cedula='80123456789',
                numero_tarjeta_profesional='123456',
                especialidades=['Laboral', 'Civil'],
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
            
            print(f"✅ Abogado creado exitosamente!\n")
            print("📋 Información del Abogado:")
            print(f"  Nombre: {abogado.usuario.nombre_completo}")
            print(f"  Especialidades: {', '.join(abogado.especialidades)}")
            print(f"  Experiencia: {abogado.anos_experiencia} años")
            print(f"  Casos Exitosos: {abogado.casos_exitosos}")
            print(f"  Calificación: ⭐ {abogado.calificacion_promedio}/5.0")
            print(f"  Tarifa: ${abogado.tarifa_consulta_minuto} COP/minuto")
            print(f"  Horas/Semana: {abogado.horas_disponibles}")
            print(f"  Ubicación: {abogado.ciudad}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creando abogado: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    crear_abogado_demo()