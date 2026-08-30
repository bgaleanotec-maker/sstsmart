# app/utils/decoradores.py

from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user

def require_role(*roles):
    """Decorador que verifica roles permitidos"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.rol.nombre not in roles:
                flash(f'❌ No tienes permiso. Roles requeridos: {", ".join(roles)}', 'error')
                return redirect(url_for('dashboard.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator