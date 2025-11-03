from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')
ia_bp = Blueprint('ia', __name__, url_prefix='/ia')
juridico_bp = Blueprint('juridico', __name__, url_prefix='/juridico')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

from app.routes import auth, dashboard, reportes, ia, juridico, admin