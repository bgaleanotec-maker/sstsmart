#!/usr/bin/env python3
"""
🔐 SCRIPT PARA CREAR USUARIOS - SST SMART
Corrige el problema de usuarios no creados correctamente en seed_data

Uso: python crear_usuarios.py
"""

import sys
import os

# Agregar la ruta del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Usuario
from werkzeug.security import generate_password_hash

def crear_usuarios():
    """Crea usuarios de prueba correctamente"""
    app = create_app()
    with app.app_context():
        print("🔐 CREANDO USUARIOS SST SMART")
        print("=" * 60)
        
        # ============ USUARIOS A CREAR ============
        usuarios_data = [
            {
                'email': 'admin@sst.local',
                'nombre_completo': 'Administrador SST',
                'rol': 'Admin',
                'password': 'admin123',
                'activo': True
            },
            {
                'email': 'abogado@sst.local',
                'nombre_completo': 'Abogado SST Colombia',
                'rol': 'Abogado',
                'password': 'abogado123',
                'activo': True
            },
            {
                'email': 'responsable.sst@company.com',
                'nombre_completo': 'Responsable SST Empresa',
                'rol': 'Responsable_SST',
                'password': 'responsable123',
                'activo': True
            },
            {
                'email': 'empleado@company.com',
                'nombre_completo': 'Juan Pérez Empleado',
                'rol': 'Empleado',
                'password': 'empleado123',
                'activo': True
            }
        ]
        
        usuarios_creados = 0
        usuarios_existentes = 0
        
        for user_data in usuarios_data:
            # Verificar si usuario ya existe
            existing = Usuario.query.filter_by(email=user_data['email']).first()
            
            if existing:
                print(f"\n⚠️  USUARIO YA EXISTE: {user_data['email']}")
                print(f"   Rol: {existing.rol}")
                print(f"   Activo: {existing.activo}")
                
                # Opción: Actualizar contraseña si es necesario
                print(f"   → Actualizando contraseña...")
                existing.set_password(user_data['password'])
                db.session.commit()
                print(f"   ✅ Contraseña actualizada")
                usuarios_existentes += 1
            else:
                # Crear nuevo usuario
                print(f"\n✅ CREANDO: {user_data['email']}")
                
                usuario = Usuario(
                    email=user_data['email'],
                    nombre_completo=user_data['nombre_completo'],
                    rol=user_data['rol'],
                    activo=user_data['activo']
                )
                
                # Usar set_password para hashear correctamente
                usuario.set_password(user_data['password'])
                
                db.session.add(usuario)
                db.session.commit()
                
                print(f"   Email: {usuario.email}")
                print(f"   Rol: {usuario.rol}")
                print(f"   Contraseña: {user_data['password']}")
                usuarios_creados += 1
        
        # ============ RESUMEN ============
        print("\n" + "=" * 60)
        print("📊 RESUMEN")
        print("=" * 60)
        print(f"✅ Nuevos usuarios creados: {usuarios_creados}")
        print(f"⚠️  Usuarios actualizados: {usuarios_existentes}")
        print(f"📋 Total usuarios en BD: {Usuario.query.count()}")
        
        # ============ LISTAR TODOS LOS USUARIOS ============
        print("\n" + "=" * 60)
        print("👥 TODOS LOS USUARIOS EN LA BD")
        print("=" * 60)
        
        todos_usuarios = Usuario.query.all()
        for idx, usuario in enumerate(todos_usuarios, 1):
            estado = "✅ Activo" if usuario.activo else "❌ Inactivo"
            print(f"\n{idx}. {usuario.nombre_completo}")
            print(f"   Email: {usuario.email}")
            print(f"   Rol: {usuario.rol}")
            print(f"   Estado: {estado}")
        
        # ============ CREDENCIALES PARA USAR ============
        print("\n" + "=" * 60)
        print("🔑 CREDENCIALES PARA PROBAR")
        print("=" * 60)
        
        print("\n👤 ADMIN")
        print("   Email: admin@sst.local")
        print("   Pass:  admin123")
        
        print("\n⚖️  ABOGADO")
        print("   Email: abogado@sst.local")
        print("   Pass:  abogado123")
        
        print("\n🏢 RESPONSABLE SST")
        print("   Email: responsable.sst@company.com")
        print("   Pass:  responsable123")
        
        print("\n👷 EMPLEADO")
        print("   Email: empleado@company.com")
        print("   Pass:  empleado123")
        
        print("\n" + "=" * 60)
        print("✅ ¡USUARIOS LISTOS PARA USAR!")
        print("=" * 60)
        print("\n🌐 Accede a: http://localhost:5000/auth/login")
        print("💡 Tip: Prueba con cualquier usuario de arriba\n")
        
        return True

if __name__ == '__main__':
    try:
        crear_usuarios()
        exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)