from flask import Flask, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os
import logging

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
jwt = JWTManager()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, default_limits=[])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(config='development'):
    from app.config import CONFIGS, ProductionConfig

    app = Flask(__name__)
    config_cls = CONFIGS.get(config, CONFIGS['development'])
    if config_cls is ProductionConfig:
        config_cls.validar()
    app.config.from_object(config_cls)

    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'cursos'), exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # La API JWT queda exenta de CSRF (usa token, no cookie de sesión)
    app.config.setdefault('WTF_CSRF_TIME_LIMIT', None)

    with app.app_context():
        # Importar modelos para que estén registrados en metadata
        from app import models  # noqa: F401

        # Multi-tenancy: resolver empresa por request + filtro automático
        from app.tenancy import init_tenancy
        init_tenancy(app)

        from app.routes import (
            auth_bp, dashboard_bp, reportes_bp, ia_bp,
            juridico_bp, admin_bp, controles_bp, formacion_bp, matriz_legal_bp
        )
        from app.routes.autoevaluacion import autoevaluacion_bp
        for bp in (auth_bp, dashboard_bp, reportes_bp, ia_bp, juridico_bp,
                   admin_bp, controles_bp, formacion_bp, matriz_legal_bp,
                   autoevaluacion_bp):
            app.register_blueprint(bp)

        @app.route('/')
        def index():
            if current_user.is_authenticated:
                return redirect(url_for('dashboard.index'))
            return redirect(url_for('auth.login'))

        @app.route('/healthz')
        def healthz():
            return jsonify(status='ok')

        # Cabeceras de seguridad (docs/03-arquitectura/03)
        @app.after_request
        def _security_headers(resp):
            resp.headers.setdefault('X-Content-Type-Options', 'nosniff')
            resp.headers.setdefault('X-Frame-Options', 'DENY')
            resp.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
            resp.headers.setdefault('Permissions-Policy',
                                    'camera=(self), geolocation=(self), microphone=()')
            if not app.config.get('DEBUG'):
                resp.headers.setdefault('Strict-Transport-Security',
                                        'max-age=31536000; includeSubDomains')
            return resp

        # En desarrollo se crean tablas al vuelo; en producción usar
        # scripts/init_prod_db.py (preDeployCommand) o migraciones
        if app.config.get('DEBUG'):
            db.create_all()

        if app.config.get('SCHEDULER_ENABLED'):
            try:
                from app.tasks.scheduler import iniciar_scheduler
                iniciar_scheduler(app)
                logger.info("Scheduler de escalamiento iniciado")
            except Exception as e:
                logger.error(f"No se pudo iniciar el scheduler: {e}")

    return app
