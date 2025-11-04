from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
import logging

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
jwt = JWTManager()

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config='development'):
    app = Flask(__name__)
    
    if config == 'development':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sst.db'
        app.config['DEBUG'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://localhost/sst_prod')
        app.config['DEBUG'] = False
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-prod')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', app.config['SECRET_KEY'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
    
    # ============ INICIALIZAR EXTENSIONES ============
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    with app.app_context():
        # ============ IMPORTAR MODELOS ============
        from app.models import (
            ConsultaJuridica, DocumentoLegal, Usuario, Empleado,
            CondicionInsegura, Evento, ConfiguracionIA,
            CategoriaArea, Dependencia, RolSST, TipoReporte,
            TipoEvidencia, MetodologiaInvestigacion
        )
        
        # ============ REGISTRAR BLUEPRINTS ============
        from app.routes import (
            auth_bp, dashboard_bp, reportes_bp, ia_bp, 
            juridico_bp, admin_bp, controles_bp
        )
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(reportes_bp)
        app.register_blueprint(ia_bp)
        app.register_blueprint(juridico_bp)      # ⭐ MÓDULO JURÍDICO
        app.register_blueprint(admin_bp)
        app.register_blueprint(controles_bp)
        
        logger.info("✅ Blueprints registrados:")
        logger.info("   ├── auth_bp")
        logger.info("   ├── dashboard_bp")
        logger.info("   ├── reportes_bp")
        logger.info("   ├── ia_bp")
        logger.info("   ├── juridico_bp ⭐")
        logger.info("   ├── admin_bp")
        logger.info("   └── controles_bp")
        
        # ============ RUTA RAÍZ ============
        @app.route('/')
        def index():
            """Ruta raíz - redirige a dashboard si está autenticado, si no al login"""
            if current_user.is_authenticated:
                return redirect(url_for('dashboard.index'))
            return redirect(url_for('auth.login'))
        
        # ============ CREAR TABLAS ============
        logger.info("📊 Inicializando base de datos...")
        db.create_all()
        logger.info("✅ Base de datos inicializada")
        logger.info("   ├── Tablas SST: OK")
        logger.info("   ├── Tablas Jurídicas: consultas_juridicas, documentos_legales ⭐")
        logger.info("   └── Tablas Configuración: OK")
        
        # ============ INICIAR SCHEDULER ============
        try:
            from app.tasks.scheduler import iniciar_scheduler
            iniciar_scheduler(app)
            logger.info("✅ Scheduler de tareas automáticas iniciado")
        except ImportError:
            logger.warning("⚠️ APScheduler no instalado. Las tareas automáticas no funcionarán.")
            logger.info("   Instala con: pip install APScheduler")
        except Exception as e:
            logger.error(f"❌ Error iniciando scheduler: {str(e)}")
    
    return app