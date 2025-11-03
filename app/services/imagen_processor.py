from app import db
from app.models import CondicionInsegura, ConfiguracionIA
from app.services.gemini_service import GeminiService
import os
from datetime import datetime
import hashlib

class ImagenProcessor:
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    @staticmethod
    def es_imagen_valida(archivo):
        if not archivo or archivo.filename == '':
            return False, "Archivo no seleccionado"
        
        ext = archivo.filename.rsplit('.', 1)[1].lower() if '.' in archivo.filename else ''
        
        if ext not in ImagenProcessor.ALLOWED_EXTENSIONS:
            return False, f"Formato no permitido"
        
        if len(archivo.read()) > ImagenProcessor.MAX_FILE_SIZE:
            return False, "Archivo demasiado grande (máx 10MB)"
        
        archivo.seek(0)
        return True, "OK"
    
    @staticmethod
    def guardar_imagen(archivo, reporte_id):
        año = datetime.utcnow().year
        mes = datetime.utcnow().month
        ruta_base = f"uploads/reportes/{año}/{mes:02d}"
        
        os.makedirs(ruta_base, exist_ok=True)
        
        contenido = archivo.read()
        hash_archivo = hashlib.md5(contenido).hexdigest()
        ext = archivo.filename.rsplit('.', 1)[1].lower()
        nombre_archivo = f"{reporte_id}_{hash_archivo}.{ext}"
        
        ruta_completa = os.path.join(ruta_base, nombre_archivo)
        
        with open(ruta_completa, 'wb') as f:
            f.write(contenido)
        
        return ruta_completa
    
    @staticmethod
    def procesar_con_ia(reporte_id):
        reporte = CondicionInsegura.query.get(reporte_id)
        if not reporte or not reporte.imagen_url:
            return {"error": "Reporte o imagen no encontrada"}
        
        try:
            gemini_service = GeminiService()
            resultado = gemini_service.analizar_imagen_sst(reporte.imagen_url)
            
            if "error" not in resultado:
                reporte.imagen_procesada_json = resultado
                reporte.observaciones_ia = resultado.get("observaciones", "")
                reporte.riesgos_identificados = resultado.get("peligros", [])
                reporte.severidad_calculada = resultado.get("severidad", 0)
                reporte.cumple_norma = reporte.severidad_calculada <= 2
                
                db.session.commit()
                return resultado
            
            return resultado
        except Exception as e:
            return {"error": str(e)}
