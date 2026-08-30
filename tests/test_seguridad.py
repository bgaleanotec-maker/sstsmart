# -*- coding: utf-8 -*-
"""Tests de seguridad: CSRF, cabeceras y healthcheck."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from app import create_app, db


@pytest.fixture()
def app():
    os.environ['SCHEDULER_ENABLED'] = '0'
    app = create_app('development')
    app.config.update(TESTING=True,
                      SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def test_healthz(app):
    r = app.test_client().get('/healthz')
    assert r.status_code == 200
    assert r.get_json()['status'] == 'ok'


def test_cabeceras_seguridad(app):
    r = app.test_client().get('/healthz')
    assert r.headers['X-Content-Type-Options'] == 'nosniff'
    assert r.headers['X-Frame-Options'] == 'DENY'
    assert 'Referrer-Policy' in r.headers


def test_csrf_bloquea_post_sin_token(app):
    # CSRF activo (no lo desactivamos en esta fixture)
    r = app.test_client().post('/auth/login',
                               data={'email': 'x@x.co', 'password': 'y'})
    assert r.status_code == 400  # Flask-WTF: The CSRF token is missing


def test_login_con_token_funciona(app):
    c = app.test_client()
    page = c.get('/auth/login').get_data(as_text=True)
    import re
    m = re.search(r'name="csrf_token" value="([^"]+)"', page)
    assert m, "el login debe renderizar el csrf_token"
    r = c.post('/auth/login', data={'email': 'no@existe.co', 'password': 'x',
                                    'csrf_token': m.group(1)})
    assert r.status_code == 200  # credenciales inválidas, pero CSRF pasó


def test_api_token_exenta_de_csrf(app):
    r = app.test_client().post('/auth/api/token',
                               json={'email': 'x@x.co', 'password': 'y'})
    assert r.status_code == 401  # rechaza credenciales, no por CSRF
