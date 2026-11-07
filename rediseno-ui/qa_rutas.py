# -*- coding: utf-8 -*-
"""QA del rediseño: recorre todas las rutas GET con el usuario admin del
entorno de desarrollo y falla si alguna devuelve 500 o lanza excepción
(rediseno-ui/README.md §9.2, versión sin Playwright: usa el cliente de
pruebas de Flask). También marca restos del tema oscuro en el HTML.

Uso (desde la raíz del repo):
    SCHEDULER_ENABLED=0 venv/Scripts/python.exe rediseno-ui/qa_rutas.py
Salida: lista de rutas con su código; código de salida 1 si hubo fallos.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db  # noqa: E402
from app.models import Usuario, Empresa  # noqa: E402

OMITIR_ENDPOINTS = {'static', 'auth.logout', 'index'}
OMITIR_SI_CONTIENE = ('export', 'descargar', 'imprimir', 'api/token')
RESTOS = re.compile(r'class="dark"|glass-card|bg-slate-900|text-slate-400')


def main():
    app = create_app('development')
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with app.app_context():
        admin = Usuario.query.filter_by(email='admin@sst.local').first()
        if not admin:
            emp = Empresa.query.first() or Empresa(nit='000000000', razon_social='Mi Empresa',
                                                   num_trabajadores=10)
            db.session.add(emp)
            db.session.commit()
            admin = Usuario(email='admin@sst.local', nombre_completo='Administrador SST',
                            rol='Admin', activo=True, empresa_id=emp.id)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

    c = app.test_client()
    r = c.post('/auth/login', data={'email': 'admin@sst.local', 'password': 'admin123'})
    assert r.status_code in (200, 302), 'no se pudo iniciar sesión'

    resultados = []
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        if 'GET' not in rule.methods or rule.endpoint in OMITIR_ENDPOINTS:
            continue
        if rule.rule.startswith('/static') or any(x in rule.rule for x in OMITIR_SI_CONTIENE):
            continue
        url = re.sub(r'<(?:int:)?\w+>', '1', rule.rule)
        try:
            resp = c.get(url, follow_redirects=False)
            code = resp.status_code
            extra = ''
            if code == 200 and 'text/html' in resp.content_type:
                html = resp.get_data(as_text=True)
                restos = sorted(set(RESTOS.findall(html)))
                if restos and rule.endpoint not in ('auth.login',):
                    extra = ' [restos: ' + ', '.join(restos) + ']'
        except Exception as e:  # noqa: BLE001
            code, extra = 'EXC', f' {type(e).__name__}: {str(e)[:90]}'
        resultados.append((code, url, rule.endpoint, extra))

    fallos = [x for x in resultados if x[0] in (500, 'EXC') or x[3].startswith(' [restos')]
    for code, url, ep, extra in resultados:
        print(('!! ' if (code in (500, 'EXC')) else '   ') + f'{code} {url} ({ep}){extra}')
    print(f'\nrutas GET probadas: {len(resultados)} · fallos: {len(fallos)} · '
          f'404 (sin datos): {sum(1 for x in resultados if x[0] == 404)}')
    return 1 if fallos else 0


if __name__ == '__main__':
    os.environ.setdefault('SCHEDULER_ENABLED', '0')
    sys.exit(main())
