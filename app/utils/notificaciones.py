import os
import logging
from flask import render_template_string, url_for
from app import db
from app.models import Usuario, Notificacion
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)

class NotificationService:
    
    @staticmethod
    def enviar_email(to_email, subject, html_content):
        """Envía un correo usando SendGrid."""
        api_key = os.getenv('SENDGRID_API_KEY')
        if not api_key:
            print("\n" + "="*50)
            print(f"📧 SIMULACIÓN DE ENVÍO DE CORREO")
            print(f"PARA: {to_email}")
            print(f"ASUNTO: {subject}")
            print("-" * 50)
            print(html_content)
            print("="*50 + "\n")
            logger.warning("⚠️ SENDGRID_API_KEY no configurada. Correo impreso en consola.")
            return True # Retornamos True para que el flujo continúe sin errores en Dev
            
        message = Mail(
            from_email=os.getenv('SENDGRID_FROM_EMAIL', 'no-reply@sst-smart.com'),
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        try:
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)
            logger.info("✅ Correo enviado a %s. Status: %s", to_email, response.status_code)
            return True
        except Exception as e:
            logger.error("❌ Error enviando correo: %s", str(e))
            return False

    @staticmethod
    def notificar_usuario(usuario_id, mensaje, tipo='info', link=None, subject=None):
        """Crea notificación en DB y opcionalmente envía correo si es crítico."""
        try:
            # 1. Crear Notificación en App
            notif = Notificacion(
                usuario_id=usuario_id,
                mensaje=mensaje,
                tipo=tipo,
                link=link
            )
            db.session.add(notif)
            db.session.commit()
            
            # 2. Enviar Correo (si hay subject)
            if subject:
                user = Usuario.query.get(usuario_id)
                if user and user.email:
                    # Template simple para email
                    html = f"""
                    <div style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
                        <h2 style="color: #2563eb;">{subject}</h2>
                        <p>{mensaje}</p>
                        {f'<a href="{link}" style="background:#2563eb;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">Ver Detalles</a>' if link else ''}
                        <hr>
                        <p style="font-size:12px; color:#888;">SST Smart System</p>
                    </div>
                    """
                    NotificationService.enviar_email(user.email, subject, html)
                    
        except Exception as e:
            logger.error("Error en notificar_usuario: %s", str(e))
            db.session.rollback()

    @staticmethod
    def notificar_rol(rol_nombre, mensaje, tipo='info', link=None, subject=None):
        """Notifica a TODOS los usuarios que tengan un rol específico."""
        users = Usuario.query.filter_by(rol=rol_nombre, activo=True).all()
        count = 0
        for user in users:
            NotificationService.notificar_usuario(user.id, mensaje, tipo, link, subject)
            count += 1
        logger.info("📢 Notificación enviada a %d usuarios con rol %s", count, rol_nombre)
