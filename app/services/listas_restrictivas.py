# -*- coding: utf-8 -*-
"""Consulta de listas vinculantes para la debida diligencia (SARLAFT/SAGRILAFT).

Solo fuentes públicas y de descarga abierta, sin eludir ningún control
(empresa/CLAUDE.md, "legal primero en datos públicos"):
- Lista consolidada del Consejo de Seguridad de la ONU: XML público. Se descarga
  si `LISTA_ONU_URL` está configurada; se guarda en memoria por proceso durante
  `LISTA_CACHE_HORAS`.
- OFAC (SDN) y otras listas: enlace para consulta manual; el resultado lo
  registra el usuario.

El emparejamiento es por nombre normalizado (sin tildes ni puntuación) con
dos criterios: todos los tokens de la consulta aparecen en la entrada, o la
similitud de difflib supera 0,88. Es una ayuda: toda coincidencia la revisa
una persona antes de bloquear a nadie.
"""
import re
import time
import unicodedata
from difflib import SequenceMatcher
import xml.etree.ElementTree as ET

_CACHE = {'entradas': None, 'cargada_en': 0.0, 'fuente': None}

ENLACES_MANUALES = [
    ('ONU — lista consolidada del Consejo de Seguridad', 'https://main.un.org/securitycouncil/es/content/un-sc-consolidated-list'),
    ('OFAC — Sanctions List Search (SDN)', 'https://sanctionssearch.ofac.treas.gov/'),
    ('Unión Europea — mapa de sanciones', 'https://www.sanctionsmap.eu/'),
]


def normalizar(texto):
    t = unicodedata.normalize('NFKD', texto or '')
    t = ''.join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r'[^a-z0-9 ]+', ' ', t.lower())
    return ' '.join(t.split())


def cargar_onu(xml_bytes):
    """Parsea la lista consolidada (INDIVIDUALS y ENTITIES) → [(nombre, tipo, ref)]."""
    raiz = ET.fromstring(xml_bytes)
    entradas = []
    for ind in raiz.iter('INDIVIDUAL'):
        partes = [ind.findtext(k) or '' for k in ('FIRST_NAME', 'SECOND_NAME', 'THIRD_NAME', 'FOURTH_NAME')]
        nombre = ' '.join(p for p in partes if p).strip()
        ref = ind.findtext('REFERENCE_NUMBER') or ''
        if nombre:
            entradas.append((nombre, 'persona', ref))
        for alias in ind.iter('INDIVIDUAL_ALIAS'):
            a = (alias.findtext('ALIAS_NAME') or '').strip()
            if a:
                entradas.append((a, 'persona (alias)', ref))
    for ent in raiz.iter('ENTITY'):
        nombre = (ent.findtext('FIRST_NAME') or '').strip()
        ref = ent.findtext('REFERENCE_NUMBER') or ''
        if nombre:
            entradas.append((nombre, 'entidad', ref))
        for alias in ent.iter('ENTITY_ALIAS'):
            a = (alias.findtext('ALIAS_NAME') or '').strip()
            if a:
                entradas.append((a, 'entidad (alias)', ref))
    return entradas


def buscar(nombre, entradas, umbral=0.88):
    """Coincidencias de `nombre` en `entradas` [(nombre, tipo, ref)]."""
    q = normalizar(nombre)
    if len(q) < 4:
        return []
    tokens = set(q.split())
    resultados = []
    for n, tipo, ref in entradas:
        nn = normalizar(n)
        if not nn:
            continue
        ntok = set(nn.split())
        if tokens <= ntok:
            puntaje = 1.0
        else:
            puntaje = SequenceMatcher(None, q, nn).ratio()
            if puntaje < umbral:
                continue
        resultados.append({'nombre': n, 'tipo': tipo, 'referencia': ref, 'similitud': round(puntaje, 2)})
    resultados.sort(key=lambda r: -r['similitud'])
    return resultados[:10]


def lista_onu(url, cache_horas=24, timeout=20):
    """Entradas de la lista ONU (descarga con caché por proceso). None si no hay URL o falla."""
    if not url:
        return None
    ahora = time.time()
    if _CACHE['entradas'] is not None and ahora - _CACHE['cargada_en'] < cache_horas * 3600:
        return _CACHE['entradas']
    try:
        import requests
        r = requests.get(url, timeout=timeout, headers={'User-Agent': 'Justrabajo-cumplimiento/1.0'})
        r.raise_for_status()
        entradas = cargar_onu(r.content)
    except Exception:
        return None
    _CACHE.update(entradas=entradas, cargada_en=ahora, fuente=url)
    return entradas


def consultar(nombre, url=None, entradas=None):
    """Resultado para registrar en la contraparte.
    → (disponible, coincidencias, fuente)"""
    if entradas is None:
        entradas = lista_onu(url)
    if entradas is None:
        return False, [], None
    return True, buscar(nombre, entradas), 'ONU lista consolidada (consulta automática)'
