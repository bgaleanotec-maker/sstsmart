from flask import Blueprint
from app.routes.controles import controles_bp

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')
ia_bp = Blueprint('ia', __name__, url_prefix='/ia')
juridico_bp = Blueprint('juridico', __name__, url_prefix='/juridico')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

from app.routes import auth, dashboard, reportes, ia, juridico, admin

__all__ = ['auth_bp', 'dashboard_bp', 'reportes_bp', 'ia_bp', 'juridico_bp', 'admin_bp', 'controles_bp']