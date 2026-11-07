from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from app.routes import dashboard_bp
from app.services.panel import datos_panel
from app.modulos import modulos_de_empresa
from app.ui import empresa_actual


@dashboard_bp.route('/')
@login_required
def index():
    """Panel "Así va tu SG-SST" (rediseno-ui/README.md §4). La lógica vive en
    app/services/panel.py para poder probarla sin HTTP.

    Las cuentas de práctica jurídica (vertical CRM Legal) no ven el panel SST:
    van a su propia pantalla de inicio.
    """
    emp = empresa_actual()
    if emp is not None and getattr(emp, 'es_practica_juridica', False):
        return redirect(url_for('crm_legal.hoy'))
    datos = datos_panel(emp, modulos_de_empresa())
    return render_template('dashboard/index.html', **datos)
