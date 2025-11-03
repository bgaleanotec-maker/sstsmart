from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
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
        # ============ REGISTRAR BLUEPRINTS ============
        from app.routes import auth_bp, dashboard_bp, reportes_bp, ia_bp, juridico_bp, admin_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(reportes_bp)
        app.register_blueprint(ia_bp)
        app.register_blueprint(juridico_bp)
        app.register_blueprint(admin_bp)
        
        # ============ CREAR TABLAS ============
        db.create_all()
        logger.info("✅ Base de datos inicializada")
        
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