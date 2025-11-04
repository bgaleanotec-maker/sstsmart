# app/services/auditoria_service.py
"""
Servicio de auditoría para tracking completo
"""

from app import db
from app.models import AuditoriaConsulta
from datetime import datetime
import json

class AuditoriaService:
    """Servicio centralizado de auditoría"""
    
    @staticmethod
    def registrar(usuario_id, accion, entidad='', entidad_id=None, razon='', detalles=None, 
                 ip_origen='', navegador=''):
        """
        Registra una acción en la auditoría
        
        Args:
            usuario_id: ID del usuario que realiza la acción
            accion: Tipo de acción (crear, modificar, eliminar, etc)
            entidad: Tipo de entidad (ConsultaJuridica, DocumentoLegal, etc)
            entidad_id: ID de la entidad
            razon: Razón de la acción
            detalles: Dict con información adicional
            ip_origen: IP del cliente
            navegador: User agent del navegador
        """
        try:
            auditoria = AuditoriaConsulta(
                usuario_id=usuario_id,
                accion=f'{entidad}_{accion}' if entidad else accion,
                razon=razon,
                detalles=detalles or {},
                ip_origen=ip_origen,
                navegador=navegador
            )
            
            # Si es una consulta jurídica
            if entidad == 'ConsultaJuridica' and entidad_id:
                auditoria.consulta_id = entidad_id
            
            db.session.add(auditoria)
            db.session.commit()
            
            return auditoria
        
        except Exception as e:
            print(f"Error registrando auditoría: {str(e)}")
            db.session.rollback()
    
    @staticmethod
    def obtener_historial(consulta_id, limite=50):
        """Obtiene historial de auditoría de una consulta"""
        return AuditoriaConsulta.query.filter_by(
            consulta_id=consulta_id
        ).order_by(AuditoriaConsulta.fecha.desc()).limit(limite).all()