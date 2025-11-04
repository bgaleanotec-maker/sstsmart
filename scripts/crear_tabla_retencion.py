#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para crear tabla de retención predefinida
Uso: python scripts/crear_tabla_retencion.py
"""

import sys
import os

# Agregar la ruta del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import TablaRetencion, TablasRetencionPredefinidas

def crear_tabla_retencion():
    """Crea tabla de retención predefinida"""
    app = create_app()
    
    with app.app_context():
        print("🌱 Creando tabla de retención predefinida...")
        print("=" * 60)
        
        # Verificar si existen
        existentes = TablaRetencion.query.count()
        
        if existentes > 0:
            print(f"⚠️  Ya existen {existentes} registros de retención")
            print("¿Deseas sobrescribir? (s/n): ", end="")
            respuesta = input().lower()
            
            if respuesta != 's':
                print("✓ Operación cancelada")
                return
            
            # Eliminar existentes
            print("🗑️  Eliminando registros existentes...")
            TablaRetencion.query.delete()
            db.session.commit()
        
        # Crear predefinidas
        print("\n📋 Creando tablas predefinidas...\n")
        
        for idx, tabla_data in enumerate(TablasRetencionPredefinidas.PREDEFINIDAS, 1):
            try:
                tabla = TablaRetencion(
                    codigo=tabla_data['codigo'],
                    tipo_documento=tabla_data['tipo_documento'],
                    tiempo_retencion_anos=tabla_data['tiempo_retencion_anos'],
                    disposicion_final=tabla_data['disposicion_final'],
                    normativa_aplicable=tabla_data['normativa_aplicable'],
                    activa=True
                )
                
                db.session.add(tabla)
                
                print(f"  {idx}. ✅ {tabla_data['codigo']} - {tabla_data['tipo_documento']}")
                print(f"     Retención: {tabla_data['tiempo_retencion_anos']} años")
                print(f"     Disposición: {tabla_data['disposicion_final']}")
                print()
            
            except Exception as e:
                print(f"  ❌ Error creando {tabla_data['codigo']}: {str(e)}\n")
        
        # Guardar
        try:
            db.session.commit()
            print("=" * 60)
            print(f"✅ Tabla de retención creada exitosamente!")
            print(f"✓ Total de registros: {TablaRetencion.query.count()}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error guardando tabla de retención: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    crear_tabla_retencion()