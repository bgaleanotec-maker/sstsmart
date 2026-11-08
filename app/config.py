"""Configuración por entornos.

Toda credencial vive en variables de entorno (.env local, panel del hosting
en producción). Nunca incrustar claves en el código: este archivo va a git.
"""
import os


def _db_url(url):
    """Render/Heroku entregan postgres:// pero SQLAlchemy 2 exige postgresql://."""
    if url and url.startswith('postgres://'):
        return url.replace('postgres://', 'postgresql://', 1)
    return url


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-prod')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploads
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB (videos de formación)
    UPLOAD_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'jpeg', 'png'}

    # Integraciones
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    SENDGRID_FROM_EMAIL = os.getenv('SENDGRID_FROM_EMAIL', 'no-reply@justrabajo.co')

    # URL pública para links en correos (en dev: localhost)
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')

    # Número de WhatsApp para el CTA de la landing (formato 573001234567)
    CONTACT_WHATSAPP = os.getenv('CONTACT_WHATSAPP', '')

    # Cumplimiento: URL del XML público de la lista consolidada de la ONU para la
    # verificación automática de contrapartes. Vacía = solo consulta manual.
    LISTA_ONU_URL = os.getenv('LISTA_ONU_URL', '')

    # Scheduler de escalamiento (apagar en workers múltiples / migraciones)
    SCHEDULER_ENABLED = os.getenv('SCHEDULER_ENABLED', '1') == '1'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = _db_url(os.getenv('DATABASE_URL', 'sqlite:///sst.db'))


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = _db_url(os.getenv('DATABASE_URL', ''))

    @classmethod
    def validar(cls):
        faltantes = []
        if not os.getenv('SECRET_KEY'):
            faltantes.append('SECRET_KEY')
        if not cls.SQLALCHEMY_DATABASE_URI:
            faltantes.append('DATABASE_URL')
        if faltantes:
            raise RuntimeError(
                f"Producción requiere variables de entorno: {', '.join(faltantes)}"
            )


CONFIGS = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
