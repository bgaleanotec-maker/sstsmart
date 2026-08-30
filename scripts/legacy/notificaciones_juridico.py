# app/services/notificaciones_juridico.py
"""
Notificaciones específicas del módulo jurídico
"""

from app.services.notificaciones import NotificacionService
from datetime import datetime

class NotificacionesJuridico(NotificacionService):
    """Extensión de notificaciones para módulo jurídico"""
    
    @staticmethod
    def enviar_asignacion_consulta(abogado, consulta):
        """Notifica abogado sobre nueva consulta asignada"""
        html = f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    max-width: 600px; margin: 0 auto; background-color: #f5f5f5;">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h2 style="margin: 0; font-size: 24px;">⚖️ Nueva Consulta Jurídica Asignada</h2>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">SST Smart - Sistema de Gestión</p>
            </div>
            
            <!-- Content -->
            <div style="background-color: white; padding: 30px; border-radius: 0 0 10px 10px;">
                <p style="color: #333; margin-bottom: 20px;">Estimado/a <strong>{abogado.nombre_completo}</strong>,</p>
                
                <p style="color: #555; line-height: 1.6; margin-bottom: 20px;">
                    Se le ha asignado una nueva consulta jurídica que requiere su atención especializada.
                </p>
                
                <!-- Detalles de la consulta -->
                <div style="background-color: #f8f9fa; border-left: 4px solid #667eea; 
                            padding: 15px; margin: 20px 0; border-radius: 4px;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr style="border-bottom: 1px solid #e0e0e0;">
                            <td style="padding: 10px 0; color: #666; font-weight: bold;">Número Consulta:</td>
                            <td style="padding: 10px 0; color: #333;">{consulta.numero_consulta}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #e0e0e0;">
                            <td style="padding: 10px 0; color: #666; font-weight: bold;">Título:</td>
                            <td style="padding: 10px 0; color: #333;">{consulta.titulo}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #e0e0e0;">
                            <td style="padding: 10px 0; color: #666; font-weight: bold;">Tipo:</td>
                            <td style="padding: 10px 0; color: #333;">{consulta.tipo_consulta}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #e0e0e0;">
                            <td style="padding: 10px 0; color: #666; font-weight: bold;">Prioridad:</td>
                            <td style="padding: 10px 0; color: #d32f2f; font-weight: bold;">{consulta.prioridad}</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #e0e0e0;">
                            <td style="padding: 10px 0; color: #666; font-weight: bold;">Riesgo Legal:</td>
                            <td style="padding: 10px 0; color: #f57c00; font-weight: bold;">{consulta.riesgo_legal}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px 0; color: #666; font-weight: bold;">Horas Estimadas:</td>
                            <td style="padding: 10px 0; color: #333;">
                                {f'{consulta.horas_estimadas} horas' if consulta.horas_estimadas else 'Por definir'}
                            </td>
                        </tr>
                    </table>
                </div>
                
                <!-- Descripción -->
                <div style="background-color: #fff3e0; border-left: 4px solid #ffa726; 
                            padding: 15px; margin: 20px 0; border-radius: 4px;">
                    <h3 style="margin: 0 0 10px 0; color: #d97706;">Descripción:</h3>
                    <p style="margin: 0; color: #555; line-height: 1.6;">
                        {consulta.descripcion[:500]}{'...' if len(consulta.descripcion) > 500 else ''}
                    </p>
                </div>
                
                <!-- Acciones -->
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://sstsmart.local/juridico/{consulta.id}" 
                       style="background-color: #667eea; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; font-weight: bold;
                              display: inline-block;">
                        Ver Consulta Completa
                    </a>
                </div>
                
                <!-- Recordatorio -->
                <div style="background-color: #e8eaf6; border-left: 4px solid #667eea; 
                            padding: 15px; margin: 20px 0; border-radius: 4px;">
                    <p style="margin: 0; color: #555; font-size: 14px;">
                        <strong>Recordatorio:</strong> Por favor revise la consulta y emita su concepto 
                        jurídico dentro de los tiempos acordados. Toda la documentación debe ser 
                        clasificada según normativa SST.
                    </p>
                </div>
                
            </div>
            
            <!-- Footer -->
            <div style="text-align: center; padding: 20px; color: #999; font-size: 12px;">
                <p>Este es un mensaje automático de SST Smart. No responda a este correo.</p>
            </div>
        </div>
        """
        
        return NotificacionService.enviar_email(
            abogado.email,
            f"[SST SMART] Nueva Consulta Jurídica - {consulta.numero_consulta}",
            html
        )
    
    @staticmethod
    def enviar_concepto_listo(usuario, consulta):
        """Notifica que el concepto jurídico está listo"""
        html = f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    max-width: 600px; margin: 0 auto;">
            
            <div style="background: linear-gradient(135deg, #00c853 0%, #1de9b6 100%); 
                        color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h2 style="margin: 0;">✅ Concepto Jurídico Emitido</h2>
            </div>
            
            <div style="background-color: white; padding: 30px; border-radius: 0 0 10px 10px;">
                <p>Estimado/a {usuario.nombre_completo},</p>
                
                <p style="color: #555;">Su consulta jurídica <strong>{consulta.numero_consulta}</strong> 
                   ha sido resuelta. El concepto jurídico está disponible.</p>
                
                <div style="background-color: #e8f5e9; border-left: 4px solid #4caf50; padding: 15px; margin: 20px 0;">
                    <p style="margin: 0; font-weight: bold;">Concepto jurídico resumido:</p>
                    <p style="margin: 10px 0 0 0; color: #333; line-height: 1.6;">
                        {consulta.concepto_legal[:300] if consulta.concepto_legal else 'Pendiente'}...
                    </p>
                </div>
                
                <div style="text-align: center; margin: 20px 0;">
                    <a href="http://sstsmart.local/juridico/{consulta.id}" 
                       style="background-color: #4caf50; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        Ver Concepto Completo
                    </a>
                </div>
            </div>
        </div>
        """
        
        return NotificacionService.enviar_email(
            usuario.email,
            f"[SST SMART] Concepto Jurídico Disponible - {consulta.numero_consulta}",
            html
        )
    
    @staticmethod
    def enviar_nuevo_comentario(usuario, consulta, comentario):
        """Notifica nuevo comentario en consulta"""
        html = f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    max-width: 600px; margin: 0 auto;">
            
            <div style="background-color: #2196F3; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0;">
                <h2 style="margin: 0;">💬 Nuevo Comentario en Consulta</h2>
            </div>
            
            <div style="background-color: white; padding: 30px; border-radius: 0 0 10px 10px;">
                <p>Estimado/a {usuario.nombre_completo},</p>
                
                <p style="color: #555;">Ha habido un nuevo comentario en la consulta jurídica:</p>
                
                <div style="background-color: #e3f2fd; border-left: 4px solid #2196F3; padding: 15px; margin: 20px 0;">
                    <p style="margin: 0; font-weight: bold;">{comentario.usuario.nombre_completo} escribió:</p>
                    <p style="margin: 10px 0 0 0; color: #333; line-height: 1.6; font-style: italic;">
                        "{comentario.contenido[:200]}{'...' if len(comentario.contenido) > 200 else ''}"
                    </p>
                </div>
                
                <div style="text-align: center; margin: 20px 0;">
                    <a href="http://sstsmart.local/juridico/{consulta.id}" 
                       style="background-color: #2196F3; color: white; padding: 12px 30px; 
                              text-decoration: none; border-radius: 5px; display: inline-block;">
                        Ver Conversación
                    </a>
                </div>
            </div>
        </div>
        """
        
        return NotificacionService.enviar_email(
            usuario.email,
            f"[SST SMART] Nuevo Comentario - {consulta.numero_consulta}",
            html
        )
    
    @staticmethod
    def enviar_documento_vencimiento(usuario, documento):
        """Notifica sobre documento próximo a vencer"""
        dias_restantes = (documento.fecha_destruccion - datetime.utcnow()).days
        
        html = f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    max-width: 600px; margin: 0 auto;">
            
            <div style="background-color: #ff9800; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0;">
                <h2 style="margin: 0;">⚠️ Documento Próximo a Vencer</h2>
            </div>
            
            <div style="background-color: white; padding: 30px; border-radius: 0 0 10px 10px;">
                <p>Estimado/a {usuario.nombre_completo},</p>
                
                <p style="color: #555;">El siguiente documento está próximo a su fecha de destrucción:</p>
                
                <div style="background-color: #fff3cd; border-left: 4px solid #ff9800; padding: 15px; margin: 20px 0;">
                    <p style="margin: 0;"><strong>Nombre:</strong> {documento.nombre}</p>
                    <p style="margin: 10px 0 0 0;"><strong>Tipo:</strong> {documento.tipo}</p>
                    <p style="margin: 10px 0 0 0;"><strong>Fecha Destrucción:</strong> {documento.fecha_destruccion.strftime('%Y-%m-%d')}</p>
                    <p style="margin: 10px 0 0 0;"><strong>Días Restantes:</strong> <span style="color: #d32f2f; font-weight: bold;">{dias_restantes} días</span></p>
                </div>
                
                <p style="color: #555;">Por favor, tome las acciones necesarias según su política de retención.</p>
            </div>
        </div>
        """
        
        return NotificacionService.enviar_email(
            usuario.email,
            f"[SST SMART] Documento Próximo a Vencer - {documento.nombre}",
            html
        )