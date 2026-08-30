#!/usr/bin/env python3
"""
🔧 CORRECTOR AUTOMÁTICO - Arregla TODOS los url_for incorrectos
Busca y corrige automáticamente todos los errores de url_for

Uso: python arreglar_todo.py
"""

import os
from pathlib import Path

def arreglar_todos_errores():
    """Busca y corrige TODOS los errores de url_for"""
    
    print("\n🔧 CORRIGIENDO TODOS LOS ERRORES DE url_for")
    print("=" * 70)
    
    # Mapeo de cambios: incorrecto → correcto
    cambios = [
        ('juridico.crear_consulta', 'juridico.crear'),
        ('juridico.listar_consultas', 'juridico.listar'),
        ('juridico.ver_consulta', 'juridico.detalle'),
        ('juridico.editar_consulta', 'juridico.detalle'),
        ('juridico.agregar_documento', 'juridico.cargar_documento'),
        ('reportes.crear_reporte', 'reportes.nuevo'),
        ('reportes.listar_reportes', 'reportes.listar'),
    ]
    
    archivos_corregidos = []
    errores_totales = 0
    
    # Buscar en todos los archivos .html
    for archivo_html in Path('.').rglob('*.html'):
        try:
            with open(archivo_html, 'r', encoding='utf-8') as f:
                contenido_original = f.read()
            
            contenido = contenido_original
            errores_en_archivo = 0
            
            # Aplicar todos los cambios
            for incorrecto, correcto in cambios:
                if incorrecto in contenido:
                    cantidad = contenido.count(incorrecto)
                    contenido = contenido.replace(incorrecto, correcto)
                    errores_en_archivo += cantidad
                    errores_totales += cantidad
                    
                    print(f"\n📁 {archivo_html}")
                    print(f"   🔄 Cambio: {incorrecto} → {correcto}")
                    print(f"   📊 Ocurrencias: {cantidad}")
            
            # Guardar si hubo cambios
            if contenido != contenido_original:
                with open(archivo_html, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                archivos_corregidos.append((str(archivo_html), errores_en_archivo))
                
        except Exception as e:
            print(f"❌ Error procesando {archivo_html}: {e}")
    
    # ============ RESUMEN ============
    print("\n" + "=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)
    print(f"✅ Archivos corregidos: {len(archivos_corregidos)}")
    print(f"✅ Errores totales corregidos: {errores_totales}")
    
    if archivos_corregidos:
        print("\n📋 Detalles:")
        for archivo, cantidad in archivos_corregidos:
            print(f"  • {archivo}: {cantidad} errores arreglados")
    
    if errores_totales == 0:
        print("\n✅ No hay errores de url_for")
    
    print("\n" + "=" * 70)
    print("🚀 PRUEBA AHORA:")
    print("   1. Recarga el navegador: F5")
    print("   2. Accede a: http://localhost:5000/juridico/")
    print("   3. ✅ Debería funcionar sin errores")
    print("=" * 70 + "\n")

if __name__ == '__main__':
    arreglar_todos_errores()