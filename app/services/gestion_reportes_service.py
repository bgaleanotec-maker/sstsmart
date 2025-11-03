from app import db
from app.models import (
    GestionReporte, GestorResponsabilidades, TareaGestion, Usuario,
    CondicionInsegura, NivelRiesgo, MatrizRiesgos
)
from datetime import datetime, timedelta
from sqlalchemy import and_, or_
from app.services.notificaciones import NotificacionService

class GestionReportesService:
    """Servicio para gestionar automáticamente los reportes SST"""
    
    @staticmethod
    def asignar_reporte(reporte_id):
        """
        Asigna automáticamente un reporte al gestor correcto basado en:
        1. Tipo de reporte
        2. Nivel de riesgo (probabilidad x severidad)
        3. GestorResponsabilidades configurado
        """
        reporte = CondicionInsegura.query.get(reporte_id)
        if not reporte:
            return None
        
        # Obtener tipo de reporte e información
        tipo_reporte = reporte.tipo_reporte_obj
        tipo_evidencia = reporte.tipo_evidencia_obj
        
        # Buscar configuración de gestor responsable
        gestor_config = GestorResponsabilidades.query.filter_by(
            tipo_reporte_id=reporte.tipo_reporte_id,
            activo=True
        ).first()
        
        if not gestor_config:
            # Fallback: buscar por nivel de riesgo si existe
            gestor_config = GestorResponsabilidades.query.filter(
                GestorResponsabilidades.tipo_reporte_id == None,
                GestorResponsabilidades.activo == True
            ).first()
        
        if not gestor_config:
            return None  # No hay configuración
        
        # Buscar usuario con rol principal
        gestor_principal = Usuario.query.filter_by(
            rol=gestor_config.rol_principal,
            activo=True
        ).first()
        
        if not gestor_principal:
            # Si no hay, usar backup
            gestor_principal = Usuario.query.filter_by(
                rol=gestor_config.rol_backup_1,
                activo=True
            ).first()
        
        if not gestor_principal:
            # Último recurso: cualquier admin
            gestor_principal = Usuario.query.filter_by(
                rol='Admin',
                activo=True
            ).first()
        
        if not gestor_principal:
            return None  # No hay gestor disponible
        
        # Crear gestión del reporte
        gestion = GestionReporte(
            reporte_id=reporte_id,
            gestor_actual_id=gestor_principal.id,
            rol_gestor=gestor_config.rol_principal,
            gestor_responsabilidad_id=gestor_config.id,
            estado='Asignado',
            fecha_asignacion=datetime.utcnow()
        )
        
        # Calcular vencimientos
        gestion.calcular_vencimientos(
            gestor_config.tiempo_respuesta_minutos,
            gestor_config.tiempo_resolucion_minutos
        )
        
        # Registrar en historial
        gestion.agregar_cambio(
            gestor_principal.id,
            'ASIGNACION_AUTOMATICA',
            f'Asignado automáticamente a {gestor_principal.nombre_completo}'
        )
        
        db.session.add(gestion)
        db.session.commit()
        
        # Crear tarea
        GestionReportesService.crear_tarea(gestion, gestor_principal)
        
        # Enviar notificación
        NotificacionService.enviar_asignacion_reporte(gestion, gestor_principal)
        
        # Notificar a roles adicionales si aplica
        if gestor_config.notificar_roles:
            NotificacionService.notificar_cc_roles(gestion, gestor_config.notificar_roles)
        
        return gestion
    
    @staticmethod
    def crear_tarea(gestion, usuario):
        """Crea una tarea para el gestor"""
        reporte = gestion.reporte
        
        tarea = TareaGestion(
            gestion_reporte_id=gestion.id,
            asignado_a_id=usuario.id,
            titulo=f"Gestionar incidente: {reporte.titulo}",
            descripcion=f"""
            Reporte: {reporte.numero_reporte}
            Tipo: {reporte.tipo_reporte_obj.nombre if reporte.tipo_reporte_obj else 'N/A'}
            Ubicación: {reporte.ubicacion_incidente.nombre if reporte.ubicacion_incidente else 'N/A'}
            Descripción: {reporte.descripcion[:200]}...
            
            Vencimiento de respuesta: {gestion.fecha_vencimiento_respuesta}
            Vencimiento de resolución: {gestion.fecha_vencimiento_resolucion}
            """,
            prioridad=GestionReportesService.calcular_prioridad(reporte),
            fecha_vencimiento=gestion.fecha_vencimiento_resolucion
        )
        
        db.session.add(tarea)
        db.session.commit()
        
        return tarea
    
    @staticmethod
    def calcular_prioridad(reporte):
        """
        Calcula la prioridad basado en severidad y otros factores
        1 = Baja, 2 = Media, 3 = Alta, 4 = Muy Alta, 5 = Crítica
        """
        try:
            if reporte.tipo_evidencia_obj:
                # Si es acto o condición insegura crítica
                if 'CRITICO' in reporte.tipo_evidencia_obj.codigo.upper():
                    return 5
                elif 'ALTO' in reporte.tipo_evidencia_obj.codigo.upper():
                    return 4
                elif 'MEDIO' in reporte.tipo_evidencia_obj.codigo.upper():
                    return 3
                elif 'BAJO' in reporte.tipo_evidencia_obj.codigo.upper():
                    return 2
            
            return 3  # Prioridad media por defecto
        except:
            return 3
    
    @staticmethod
    def escalonar_automatico(gestion_id):
        """
        Escalona automáticamente un reporte si:
        1. Se venció tiempo de respuesta
        2. Se venció tiempo de resolución
        """
        gestion = GestionReporte.query.get(gestion_id)
        if not gestion or not gestion.activo:
            return False
        
        gestor_config = gestion.gestor_responsabilidad
        if not gestor_config:
            return False
        
        # Determinar a quién escalona
        if gestion.numero_escalamiento == 0:
            rol_destino = gestor_config.rol_backup_1
        elif gestion.numero_escalamiento == 1:
            rol_destino = gestor_config.rol_backup_2
        else:
            # Ya escaló todo, notificar a Dirección
            rol_destino = 'Admin'
        
        if not rol_destino:
            return False
        
        # Buscar usuario con ese rol
        gestor_escalado = Usuario.query.filter_by(
            rol=rol_destino,
            activo=True
        ).first()
        
        if not gestor_escalado:
            return False
        
        # Actualizar gestión
        gestion.numero_escalamiento += 1
        gestion.gestor_actual_id = gestor_escalado.id
        gestion.rol_gestor = rol_destino
        gestion.escalado_a_id = gestor_escalado.id
        gestion.estado = 'Escalado'
        
        gestion.agregar_cambio(
            gestor_escalado.id,
            'ESCALONAMIENTO',
            f'Escalado automáticamente a {gestor_escalado.nombre_completo} (Paso {gestion.numero_escalamiento})'
        )
        
        db.session.commit()
        
        # Crear nueva tarea
        GestionReportesService.crear_tarea(gestion, gestor_escalado)
        
        # Notificar escalamiento por email
        NotificacionService.enviar_escalonamiento(gestion, gestor_escalado)
        
        return True
    
    @staticmethod
    def verificar_vencimientos():
        """
        Verifica todos los reportes en gestión y escalona si es necesario
        Se ejecuta periódicamente (via Celery, APScheduler, etc)
        """
        escalados = 0
        
        # Reportes vencidos en respuesta
        gestiones_vencidas_respuesta = GestionReporte.query.filter(
            GestionReporte.estado.in_(['Asignado', 'En_Espera']),
            GestionReporte.fecha_respuesta == None,
            GestionReporte.fecha_vencimiento_respuesta < datetime.utcnow(),
            GestionReporte.activo == True
        ).all()
        
        for gestion in gestiones_vencidas_respuesta:
            if GestionReportesService.escalonar_automatico(gestion.id):
                escalados += 1
        
        # Reportes vencidos en resolución
        gestiones_vencidas_resolucion = GestionReporte.query.filter(
            GestionReporte.estado.in_(['En_Proceso']),
            GestionReporte.fecha_resolucion == None,
            GestionReporte.fecha_vencimiento_resolucion < datetime.utcnow(),
            GestionReporte.activo == True
        ).all()
        
        for gestion in gestiones_vencidas_resolucion:
            if GestionReportesService.escalonar_automatico(gestion.id):
                escalados += 1
        
        # Notificar sobre vencimientos críticos (dentro de 30 min)
        gestiones_criticas = GestionReporte.query.filter(
            GestionReporte.estado.in_(['Asignado', 'En_Proceso']),
            GestionReporte.fecha_resolucion == None,
            GestionReporte.fecha_vencimiento_resolucion < datetime.utcnow() + timedelta(minutes=30),
            GestionReporte.fecha_vencimiento_resolucion > datetime.utcnow(),
            GestionReporte.activo == True
        ).all()
        
        for gestion in gestiones_criticas:
            NotificacionService.enviar_vencimiento_critico(gestion)
        
        return escalados
    
    @staticmethod
    def marcar_respondido(gestion_id, usuario_id):
        """Marca que el gestor respondió"""
        gestion = GestionReporte.query.get(gestion_id)
        if gestion:
            gestion.fecha_respuesta = datetime.utcnow()
            gestion.estado = 'En_Proceso'
            gestion.agregar_cambio(usuario_id, 'RESPUESTA', 'Gestor respondió')
            
            db.session.commit()
            
            # Notificar al reportador que está siendo procesado
            return True
        return False
    
    @staticmethod
    def marcar_resuelto(gestion_id, usuario_id, resolucion):
        """Marca que el gestor resolvió"""
        gestion = GestionReporte.query.get(gestion_id)
        if gestion:
            gestion.fecha_resolucion = datetime.utcnow()
            gestion.estado = 'Resuelto'
            gestion.notas_internas = resolucion
            gestion.agregar_cambio(usuario_id, 'RESOLUCION', 'Gestor resolvió: ' + resolucion)
            
            db.session.commit()
            
            # Notificar al reportador que fue resuelto
            NotificacionService.enviar_reporte_resuelto(gestion, resolucion)
            
            return True
        return False
    
    @staticmethod
    def marcar_cerrado(gestion_id, usuario_id):
        """Marca el reporte como cerrado"""
        gestion = GestionReporte.query.get(gestion_id)
        if gestion:
            gestion.estado = 'Cerrado'
            gestion.agregar_cambio(usuario_id, 'CIERRE', 'Reporte cerrado')
            gestion.activo = False
            
            db.session.commit()
            return True
        return False