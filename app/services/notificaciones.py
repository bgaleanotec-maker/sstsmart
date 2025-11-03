import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
import logging

logger = logging.getLogger(__name__)

class NotificacionService:
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'noreply@sst-system.com')
    
    @staticmethod
    def enviar_email(destinatario, asunto, contenido_html):
        try:
            sg = SendGridAPIClient(NotificacionService.SENDGRID_API_KEY)
            
            message = Mail(
                from_email=NotificacionService.SENDER_EMAIL,
                to_emails=destinatario,
                subject=asunto,
                html_content=contenido_html
            )
            
            response = sg.send(message)
            logger.info(f"Email enviado a {destinatario}")
            return True
        except Exception as e:
            logger.error(f"Error enviando email: {str(e)}")
            return False
    
    # ============== GESTIÓN DE REPORTES ==============
    
    @staticmethod
    def enviar_asignacion_reporte(gestion, gestor):
        """Notifica al gestor que un reporte fue asignado"""
        try:
            reporte = gestion.reporte
            asunto = f"[SST-ASIGNADO] {reporte.numero_reporte} - {reporte.titulo}"
            
            html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #007bff; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0;">
                    <h2 style="margin: 0;">🔔 Nuevo Reporte Asignado</h2>
                </div>
                
                <div style="background-color: #f5f5f5; padding: 20px; border-radius: 0 0 5px 5px;">
                    <p>Se te ha asignado un nuevo reporte que requiere tu atención.</p>
                    
                    <div style="background-color: white; padding: 15px; border-left: 4px solid #007bff; margin: 20px 0;">
                        <p><strong>📋 Número Reporte:</strong> {reporte.numero_reporte}</p>
                        <p><strong>📝 Título:</strong> {reporte.titulo}</p>
                        <p><strong>🏷️ Tipo:</strong> {reporte.tipo_reporte_obj.nombre if reporte.tipo_reporte_obj else 'N/A'}</p>
                        <p><strong>📍 Ubicación:</strong> {reporte.ubicacion_incidente.nombre if reporte.ubicacion_incidente else 'No especificada'}</p>
                        <p><strong>⏰ Vencimiento Respuesta:</strong> {gestion.fecha_vencimiento_respuesta.strftime('%d/%m/%Y %H:%M')}</p>
                        <p><strong>⏳ Vencimiento Resolución:</strong> {gestion.fecha_vencimiento_resolucion.strftime('%d/%m/%Y %H:%M')}</p>
                    </div>
                    
                    <p style="text-align: center; margin-top: 20px;">
                        <a href="http://localhost:5000/reportes/{reporte.id}" style="background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">Ver Reporte</a>
                    </p>
                </div>
            </div>
            """
            
            return NotificacionService.enviar_email(gestor.email, asunto, html)
        except Exception as e:
            logger.error(f"Error enviando notificación de asignación: {str(e)}")
            return False
    
    @staticmethod
    def enviar_escalonamiento(gestion, gestor_escalado):
        """Notifica que el reporte fue escalado a otro gestor"""
        try:
            reporte = gestion.reporte
            asunto = f"[SST-ESCALADO] {reporte.numero_reporte} - ⚠️ Se requiere tu atención inmediata"
            
            html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #dc3545; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0;">
                    <h2 style="margin: 0;">⚠️ Reporte Escalado</h2>
                </div>
                
                <div style="background-color: #fff3cd; padding: 20px; border-radius: 0 0 5px 5px; border-left: 4px solid #ffc107;">
                    <p><strong style="color: #dc3545;">Un reporte fue escalado a ti por falta de respuesta.</strong></p>
                    
                    <div style="background-color: white; padding: 15px; border-left: 4px solid #dc3545; margin: 20px 0;">
                        <p><strong>📋 Número Reporte:</strong> {reporte.numero_reporte}</p>
                        <p><strong>📝 Título:</strong> {reporte.titulo}</p>
                        <p><strong>🏷️ Tipo:</strong> {reporte.tipo_reporte_obj.nombre if reporte.tipo_reporte_obj else 'N/A'}</p>
                        <p><strong>🔄 Paso de Escalonamiento:</strong> {gestion.numero_escalamiento}</p>
                        <p><strong style="color: red;">⏰ Vencimiento Respuesta:</strong> {gestion.fecha_vencimiento_respuesta.strftime('%d/%m/%Y %H:%M')}</p>
                    </div>
                    
                    <p style="text-align: center; margin-top: 20px; color: red; font-weight: bold;">
                        ⏰ ACCIÓN REQUERIDA INMEDIATAMENTE
                    </p>
                    <p style="text-align: center;">
                        <a href="http://localhost:5000/reportes/{reporte.id}" style="background-color: #dc3545; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">Ver Reporte Ahora</a>
                    </p>
                </div>
            </div>
            """
            
            return NotificacionService.enviar_email(gestor_escalado.email, asunto, html)
        except Exception as e:
            logger.error(f"Error enviando notificación de escalamiento: {str(e)}")
            return False
    
    @staticmethod
    def enviar_vencimiento_critico(gestion):
        """Notifica cuando un reporte está a punto de vencer"""
        try:
            reporte = gestion.reporte
            gestor = gestion.gestor_actual
            
            asunto = f"[SST-CRÍTICO] {reporte.numero_reporte} - 🚨 Vencimiento Inminente"
            
            html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #ff0000; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0;">
                    <h2 style="margin: 0;">🚨 CRÍTICO: Reporte a Punto de Vencer</h2>
                </div>
                
                <div style="background-color: #ffe5e5; padding: 20px; border-radius: 0 0 5px 5px; border-left: 4px solid #ff0000;">
                    <p style="color: red; font-weight: bold; font-size: 16px;">El siguiente reporte está a punto de vencer y requiere ACCIÓN INMEDIATA.</p>
                    
                    <div style="background-color: white; padding: 15px; border-left: 4px solid #ff0000; margin: 20px 0;">
                        <p><strong>📋 Número Reporte:</strong> {reporte.numero_reporte}</p>
                        <p><strong>📝 Título:</strong> {reporte.titulo}</p>
                        <p><strong style="color: red; font-size: 18px;">⏰ Vencimiento:</strong> <span style="font-size: 18px; color: red;">{gestion.fecha_vencimiento_resolucion.strftime('%d/%m/%Y %H:%M')}</span></p>
                        <p><strong>Estado Actual:</strong> {gestion.estado}</p>
                    </div>
                    
                    <p style="text-align: center; margin-top: 20px;">
                        <a href="http://localhost:5000/reportes/{reporte.id}" style="background-color: #ff0000; color: white; padding: 14px 28px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold; font-size: 16px;">⚡ RESOLVER URGENTEMENTE</a>
                    </p>
                </div>
            </div>
            """
            
            return NotificacionService.enviar_email(gestor.email, asunto, html)
        except Exception as e:
            logger.error(f"Error enviando notificación crítica: {str(e)}")
            return False
    
    @staticmethod
    def enviar_reporte_resuelto(gestion, resolucion):
        """Notifica al reportador que su reporte fue resuelto"""
        try:
            reporte = gestion.reporte
            reportador = reporte.reportador
            
            asunto = f"[SST-RESUELTO] {reporte.numero_reporte} - ✅ Tu reporte ha sido atendido"
            
            html = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background-color: #28a745; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0;">
                    <h2 style="margin: 0;">✅ Reporte Resuelto</h2>
                </div>
                
                <div style="background-color: #e8f5e9; padding: 20px; border-radius: 0 0 5px 5px; border-left: 4px solid #28a745;">
                    <p>Tu reporte ha sido revisado y resuelto por el equipo de SST.</p>
                    
                    <div style="background-color: white; padding: 15px; border-left: 4px solid #28a745; margin: 20px 0;">
                        <p><strong>📋 Número Reporte:</strong> {reporte.numero_reporte}</p>
                        <p><strong>📝 Título:</strong> {reporte.titulo}</p>
                        <p><strong>📅 Fecha Resolución:</strong> {gestion.fecha_resolucion.strftime('%d/%m/%Y %H:%M')}</p>
                        <p><strong>📄 Resolución:</strong></p>
                        <p style="background-color: #f9f9f9; padding: 10px; border-radius: 3px;">{resolucion[:300]}</p>
                    </div>
                    
                    <p style="text-align: center; margin-top: 20px;">
                        <a href="http://localhost:5000/reportes/{reporte.id}" style="background-color: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">Ver Detalles Completos</a>
                    </p>
                </div>
            </div>
            """
            
            return NotificacionService.enviar_email(reportador.email, asunto, html)
        except Exception as e:
            logger.error(f"Error enviando notificación de resolución: {str(e)}")
            return False
    
    @staticmethod
    def notificar_cc_roles(gestion, roles_notificacion):
        """Envía notificación en copia a roles específicos"""
        try:
            from app.models import Usuario
            reporte = gestion.reporte
            
            usuarios = Usuario.query.filter(Usuario.rol.in_(roles_notificacion), Usuario.activo == True).all()
            
            for usuario in usuarios:
                asunto = f"[SST-CC] {reporte.numero_reporte} - Notificación de seguimiento"
                html = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background-color: #17a2b8; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0;">
                        <h2 style="margin: 0;">📢 Notificación de Seguimiento</h2>
                    </div>
                    
                    <div style="background-color: #f5f5f5; padding: 20px; border-radius: 0 0 5px 5px;">
                        <p>Se te envía una copia de la siguiente gestión para tu conocimiento y seguimiento.</p>
                        
                        <div style="background-color: white; padding: 15px; border-left: 4px solid #17a2b8; margin: 20px 0;">
                            <p><strong>📋 Número Reporte:</strong> {reporte.numero_reporte}</p>
                            <p><strong>📝 Título:</strong> {reporte.titulo}</p>
                            <p><strong>🏷️ Tipo:</strong> {reporte.tipo_reporte_obj.nombre if reporte.tipo_reporte_obj else 'N/A'}</p>
                            <p><strong>📊 Estado:</strong> {gestion.estado}</p>
                        </div>
                        
                        <p style="text-align: center; margin-top: 20px;">
                            <a href="http://localhost:5000/reportes/{reporte.id}" style="background-color: #17a2b8; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Ver Reporte</a>
                        </p>
                    </div>
                </div>
                """
                
                NotificacionService.enviar_email(usuario.email, asunto, html)
        except Exception as e:
            logger.error(f"Error enviando notificaciones CC: {str(e)}")
    
    # ============== CONSULTAS JURÍDICAS ==============
    
    @staticmethod
    def enviar_asignacion_consulta(abogado, consulta):
        """Notifica al abogado sobre nueva consulta asignada"""
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #6f42c1; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0;">
                <h2 style="margin: 0;">⚖️ Nueva Consulta Jurídica Asignada</h2>
            </div>
            
            <div style="background-color: #f5f5f5; padding: 20px; border-radius: 0 0 5px 5px;">
                <div style="background-color: white; padding: 15px; border-left: 4px solid #6f42c1; margin: 20px 0;">
                    <p><strong>📋 Número:</strong> {consulta.numero_consulta}</p>
                    <p><strong>📝 Título:</strong> {consulta.titulo}</p>
                    <p><strong>🏷️ Tipo:</strong> {consulta.tipo_consulta}</p>
                    <p><strong>⚠️ Prioridad:</strong> {consulta.prioridad}</p>
                    <p><strong>⚡ Riesgo Legal:</strong> {consulta.riesgo_legal}</p>
                    <p><strong>📄 Descripción:</strong> {consulta.descripcion[:200]}</p>
                </div>
                
                <p style="text-align: center; margin-top: 20px;">
                    <a href="http://localhost:5000/juridico/{consulta.id}" style="background-color: #6f42c1; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">Ver Consulta</a>
                </p>
            </div>
        </div>
        """
        
        return NotificacionService.enviar_email(
            abogado.email,
            f"[SST] Nueva Consulta Jurídica: {consulta.numero_consulta}",
            html
        )
    
    @staticmethod
    def enviar_resolucion_consulta(empleado, consulta):
        """Notifica al empleado cuando su consulta es resuelta"""
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #28a745; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0;">
                <h2 style="margin: 0;">✅ Consulta Jurídica Resuelta</h2>
            </div>
            
            <div style="background-color: #e8f5e9; padding: 20px; border-radius: 0 0 5px 5px;">
                <div style="background-color: white; padding: 15px; border-left: 4px solid #28a745; margin: 20px 0;">
                    <p><strong>📋 Número:</strong> {consulta.numero_consulta}</p>
                    <p><strong>📝 Título:</strong> {consulta.titulo}</p>
                    <p><strong>✅ Resolución:</strong></p>
                    <p style="background-color: #f9f9f9; padding: 10px; border-radius: 3px;">{consulta.resolucion[:300]}</p>
                    <p><strong>💡 Recomendaciones:</strong></p>
                    <p style="background-color: #f9f9f9; padding: 10px; border-radius: 3px;">{consulta.recomendaciones[:300]}</p>
                </div>
                
                <p style="text-align: center; margin-top: 20px;">
                    <a href="http://localhost:5000/juridico/{consulta.id}" style="background-color: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">Ver Detalle Completo</a>
                </p>
            </div>
        </div>
        """
        
        return NotificacionService.enviar_email(
            empleado.email,
            f"[SST] Consulta Resuelta: {consulta.numero_consulta}",
            html
        )
    
    @staticmethod
    def enviar_notificacion_reporte(responsable, reporte):
        """Notifica nuevo reporte SST"""
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #fd7e14; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0;">
                <h2 style="margin: 0;">🔔 Nuevo Reporte de Condición Insegura</h2>
            </div>
            
            <div style="background-color: #fff3cd; padding: 20px; border-radius: 0 0 5px 5px;">
                <div style="background-color: white; padding: 15px; border-left: 4px solid #fd7e14; margin: 20px 0;">
                    <p><strong>📋 Número:</strong> {reporte.numero_reporte}</p>
                    <p><strong>📝 Título:</strong> {reporte.titulo}</p>
                    <p><strong>📍 Ubicación:</strong> {reporte.ubicacion_incidente.nombre if reporte.ubicacion_incidente else 'No especificada'}</p>
                    <p><strong>⚠️ Severidad:</strong> {reporte.tipo_evidencia_obj.nombre if reporte.tipo_evidencia_obj else 'N/A'}</p>
                </div>
                
                <p style="text-align: center; margin-top: 20px;">
                    <a href="http://localhost:5000/reportes/{reporte.id}" style="background-color: #fd7e14; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">Ver Reporte</a>
                </p>
            </div>
        </div>
        """
        
        return NotificacionService.enviar_email(
            responsable.email,
            f"[SST] Nuevo Reporte: {reporte.numero_reporte}",
            html
        )