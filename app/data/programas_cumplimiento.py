# -*- coding: utf-8 -*-
"""Catálogo de programas de cumplimiento (módulo `cumplimiento`).

Un programa es un sistema de gestión exigido por una autoridad distinta de
Mintrabajo que la pyme debe documentar, operar y reportar: SARLAFT del
transporte, PTEE, SAGRILAFT y protección de datos personales. El módulo los
trata igual: lista de requisitos con evidencia, oficial o responsable,
matriz de riesgos, contrapartes con debida diligencia y reportes con fecha.

REGLA (empresa/CLAUDE.md): nada inventado. Toda norma, umbral o fecha nace con
`verificado=False` y la interfaz la marca "[VERIFICAR]" hasta que Brian confirme
la fuente oficial; los valores numéricos (UVB, UVT, SMLMV) son los últimos que
encontró la investigación del 8-nov-2026 y se cambian aquí, en un solo lugar.

Estructura de cada programa:
  nombre, nombre_largo, autoridad, icono, resumen, a_quien_aplica,
  normas: [(cita, verificado)],
  regimenes: {codigo: nombre} (el primero es el completo),
  requisitos: [dict(codigo, nombre, descripcion, etapa, regimenes, periodicidad_meses)]
     regimenes: 'todos' o tupla de códigos de régimen a los que aplica
     periodicidad_meses: None = se cumple una vez; N = se revisa cada N meses
  reportes: [dict(codigo, nombre, fechas=[(mes, dia), ...], norma, verificado)]
     fechas fijas del año; el servicio genera la próxima ocurrencia de cada una.
"""

# Parámetros usados por el diagnóstico "¿me aplica?". Fuente y fecha al lado.
PARAMETROS = {
    # Unidad de Valor Básico: COP 12.110 según nota de Garrigues (jun-2026). [VERIFICAR]
    'uvb': {'valor': 12_110, 'vigencia': '2026', 'fuente': 'Garrigues, nota 26-jun-2026 sobre Res. 7038/2026', 'verificado': False},
    # Umbral SARLAFT completo vs. Régimen de Medidas Simplificadas (ingresos al 31-dic anterior). [VERIFICAR]
    'umbral_sarlaft_uvb': {'valor': 142_206.50, 'vigencia': '2026', 'fuente': 'Supertransporte, página SARLAFT-PTEE; Acoltés sobre Circular 20265330000054/2026', 'verificado': False},
    # UVT 2026 según la convención de plataforma/README.md. [VERIFICAR contra la resolución DIAN]
    'uvt': {'valor': 52_374, 'vigencia': '2026', 'fuente': 'plataforma/README.md (convenciones); confirmar con la resolución DIAN de UVT 2026', 'verificado': False},
    # Umbral de inscripción en el RNBD: activos totales > 100.000 UVT (Decreto 090/2018). [VERIFICAR]
    'umbral_rnbd_uvt': {'valor': 100_000, 'vigencia': '2018', 'fuente': 'Decreto 090 de 2018 (cita de Gómez-Pinzón en Asuntos Legales, 2021)', 'verificado': False},
    # SMMLV 2026 según la convención de plataforma/README.md. [VERIFICAR contra el decreto de salario mínimo]
    'smlmv': {'valor': 1_750_905, 'vigencia': '2026', 'fuente': 'plataforma/README.md (convenciones); confirmar con el decreto de salario mínimo 2026', 'verificado': False},
    # Umbral SAGRILAFT (ingresos o activos, según sector): 30.000 SMLMV en varios sectores. [VERIFICAR]
    'umbral_sagrilaft_smlmv': {'valor': 30_000, 'vigencia': '2024', 'fuente': 'Circular 100-000016/2020 Supersociedades num. 4.2 (cita de Crowe)', 'verificado': False},
}


def parametro(nombre):
    return PARAMETROS[nombre]['valor']


PROGRAMAS = {
    'sarlaft_transporte': {
        'nombre': 'SARLAFT transporte',
        'nombre_largo': 'Sistema de administración del riesgo de lavado de activos, financiación del terrorismo y '
                        'financiamiento de la proliferación de armas (empresas vigiladas por la Supertransporte)',
        'autoridad': 'Superintendencia de Transporte',
        'icono': 'fa-truck-fast',
        'resumen': 'Desde 2025 reemplaza al SIPLAFT. Las empresas de transporte de carga, pasajeros, especial y mixto '
                   'deben tener política, manual, oficial de cumplimiento registrado en SIREL, matriz de riesgos, '
                   'conocimiento de contrapartes y reportes a la UIAF y a la Supertransporte.',
        'a_quien_aplica': 'Sujetos vigilados por la Supertransporte (art. 4.1.1 de la Circular Única de Infraestructura y '
                          'Transporte): transporte público de carga, pasajeros, especial, mixto, por cable, operadores '
                          'multimodales y desintegradoras, entre otros. Con ingresos del año anterior iguales o superiores '
                          'a 142.206,50 UVB aplica el SARLAFT completo; por debajo, el Régimen de Medidas Simplificadas.',
        'normas': [
            ('Resolución 2328 de 2025 de la Supertransporte (cap. 6, título V de la Circular Única)', False),
            ('Resolución 16615 de 2025 de la Supertransporte', False),
            ('Resolución 4607 de 2026 de la Supertransporte', False),
            ('Circular Externa 20265330000054 de 2026 (supervisión SARLAFT y RMS)', False),
        ],
        'regimenes': {'completo': 'SARLAFT completo', 'simplificado': 'Régimen de Medidas Simplificadas (RMS)'},
        'requisitos': [
            dict(codigo='politica', etapa='Diseño', regimenes='todos', periodicidad_meses=None,
                 nombre='Política LA/FT/FPADM aprobada por el máximo órgano social',
                 descripcion='Documento con compromiso de la dirección, funciones de los órganos y del oficial, gestión de riesgos y controles, cultura, recursos, mejora continua y reporte oportuno a la UIAF. Evidencia: acta de aprobación.'),
            dict(codigo='manual', etapa='Diseño', regimenes='todos', periodicidad_meses=None,
                 nombre='Manual del sistema (SARLAFT o RMS) con procedimientos',
                 descripcion='Procedimientos escritos de identificación, medición, control y monitoreo del riesgo; conocimiento de contrapartes; señales de alerta; reporte interno y externo.'),
            dict(codigo='oficial', etapa='Diseño', regimenes='todos', periodicidad_meses=None,
                 nombre='Designación del oficial de cumplimiento principal (o responsable en el RMS)',
                 descripcion='Acta de designación, hoja de vida, formación en administración de riesgos, residencia en Colombia e independencia. Un oficial externo puede atender hasta diez empresas vigiladas.'),
            dict(codigo='oficial_suplente', etapa='Diseño', regimenes=('completo',), periodicidad_meses=None,
                 nombre='Oficial de cumplimiento suplente designado',
                 descripcion='Mismos soportes del principal (acta, hoja de vida, certificaciones).'),
            dict(codigo='sirel', etapa='Diseño', regimenes='todos', periodicidad_meses=None,
                 nombre='Oficial registrado en el SIREL de la UIAF',
                 descripcion='Sin registro en SIREL no se pueden presentar los reportes de operaciones sospechosas. Evidencia: constancia de registro.'),
            dict(codigo='matriz', etapa='Identificación', regimenes='todos', periodicidad_meses=12,
                 nombre='Matriz de riesgos LA/FT/FPADM por factores',
                 descripcion='Riesgos por contraparte, producto o servicio, canal y jurisdicción; riesgo inherente, controles y riesgo residual. Se gestiona en la pestaña Riesgos.'),
            dict(codigo='debida_diligencia', etapa='Control', regimenes='todos', periodicidad_meses=None,
                 nombre='Procedimiento de conocimiento de contrapartes',
                 descripcion='Clientes, proveedores, empleados, socios, conductores y propietarios de vehículos vinculados: identificación, verificación en listas vinculantes (ONU, OFAC), PEP y origen de fondos. Se opera en Contrapartes.'),
            dict(codigo='senales', etapa='Control', regimenes='todos', periodicidad_meses=None,
                 nombre='Señales de alerta y procedimiento de operaciones inusuales',
                 descripcion='Listado de señales propias del negocio (pagos en efectivo atípicos, rutas sin lógica económica, terceros que pagan por el cliente) y quién las analiza.'),
            dict(codigo='ros', etapa='Reporte', regimenes='todos', periodicidad_meses=None,
                 nombre='Procedimiento de reporte de operaciones sospechosas (ROS) a la UIAF',
                 descripcion='Quién decide, en qué plazo y cómo se documenta. Los reportes periódicos aparecen en la pestaña Reportes.'),
            dict(codigo='capacitacion', etapa='Operación', regimenes='todos', periodicidad_meses=12,
                 nombre='Capacitación anual en LA/FT/FPADM con evidencias',
                 descripcion='Plan, asistencia y evaluación. La UIAF ofrece un curso virtual gratuito que sirve de evidencia.'),
            dict(codigo='divulgacion', etapa='Operación', regimenes='todos', periodicidad_meses=None,
                 nombre='Evidencias de divulgación de la política',
                 descripcion='Comunicación a empleados, contratistas y contrapartes (correos, carteleras, cláusulas contractuales).'),
            dict(codigo='informes_oficial', etapa='Monitoreo', regimenes=('completo',), periodicidad_meses=12,
                 nombre='Informes del oficial de cumplimiento al máximo órgano social',
                 descripcion='Resultados de la gestión, señales de alerta, ROS presentados y plan de mejora. Evidencia: actas.'),
            dict(codigo='auditoria', etapa='Monitoreo', regimenes=('completo',), periodicidad_meses=12,
                 nombre='Auditoría o evaluación anual del sistema',
                 descripcion='Revisoría fiscal o auditoría interna que evalúa el sistema y deja informe.'),
            dict(codigo='plan_mejoramiento', etapa='Monitoreo', regimenes='todos', periodicidad_meses=None,
                 nombre='Plan de mejoramiento de hallazgos',
                 descripcion='Hallazgos de auditoría o de la Supertransporte con responsable y fecha.'),
            dict(codigo='conservacion', etapa='Operación', regimenes='todos', periodicidad_meses=None,
                 nombre='Conservación de los soportes del sistema',
                 descripcion='Archivo físico o digital de política, actas, matriz, verificaciones y reportes por el término que fija la norma.'),
        ],
        'reportes': [
            dict(codigo='supertransporte_sarlaft', nombre='Reporte periódico de SARLAFT / RMS a la Supertransporte',
                 fechas=[(1, 10), (4, 10), (7, 10), (10, 10)],
                 norma='Circular Externa 20265330000054 de 2026 (primer reporte: 10-ago-2026; periodicidad citada por Acoltés con fechas incoherentes)',
                 verificado=False),
        ],
    },

    'ptee_transporte': {
        'nombre': 'PTEE transporte',
        'nombre_largo': 'Programa de transparencia y ética empresarial (empresas vigiladas por la Supertransporte)',
        'autoridad': 'Superintendencia de Transporte',
        'icono': 'fa-handshake-angle',
        'resumen': 'Prevención de corrupción y soborno transnacional: política, oficial o responsable de cumplimiento, '
                   'matriz de riesgos, canal de denuncias confidencial, debida diligencia y publicación en la web.',
        'a_quien_aplica': 'Personas jurídicas vigiladas por la Supertransporte. Las de ingresos hasta 142.206,50 UVB pueden '
                          'designar un responsable de cumplimiento interno en lugar de un oficial. El oficial del SARLAFT '
                          'puede asumir también el PTEE.',
        'normas': [
            ('Resolución 14673 de 2025 de la Supertransporte (cap. 10, título V de la Circular Única)', False),
            ('Resolución 7038 de 2026 de la Supertransporte (plazo al 18-ago-2026 y responsable de cumplimiento)', False),
            ('Ley 1778 de 2016 (soborno transnacional) y Ley 2195 de 2022', False),
        ],
        'regimenes': {'oficial': 'Con oficial de cumplimiento', 'responsable': 'Con responsable de cumplimiento (ingresos hasta el umbral)'},
        'requisitos': [
            dict(codigo='politica', etapa='Diseño', regimenes='todos', periodicidad_meses=None,
                 nombre='Política anticorrupción y antisoborno aprobada',
                 descripcion='Compromiso de la dirección, alcance, prohibiciones y sanciones internas. Evidencia: acta.'),
            dict(codigo='oficial', etapa='Diseño', regimenes='todos', periodicidad_meses=None,
                 nombre='Oficial o responsable de cumplimiento del PTEE designado',
                 descripcion='El responsable debe ser empleado de al menos segundo nivel jerárquico, con capacidad de decisión y reporte directo al máximo órgano social. Evidencia: acta.'),
            dict(codigo='matriz', etapa='Identificación', regimenes='todos', periodicidad_meses=12,
                 nombre='Matriz de riesgos de corrupción y soborno transnacional',
                 descripcion='Por proceso, contraparte, país y canal. Se gestiona en Riesgos.'),
            dict(codigo='canal', etapa='Control', regimenes='todos', periodicidad_meses=None,
                 nombre='Canal de denuncias confidencial con protección al denunciante',
                 descripcion='Correo, formulario o línea; procedimiento de recepción, análisis y protección frente a represalias.'),
            dict(codigo='debida_diligencia', etapa='Control', regimenes='todos', periodicidad_meses=None,
                 nombre='Debida diligencia de contrapartes y empleados expuestos',
                 descripcion='Intermediarios, contratistas y funcionarios que tratan con el Estado. Se opera en Contrapartes.'),
            dict(codigo='capacitacion', etapa='Operación', regimenes='todos', periodicidad_meses=12,
                 nombre='Capacitación anual y comunicación del programa',
                 descripcion='Asistencia, material y evaluación.'),
            dict(codigo='web', etapa='Operación', regimenes='todos', periodicidad_meses=None,
                 nombre='Publicación en la página web',
                 descripcion='Datos de contacto, línea anticorrupción, protección al denunciante, PTEE, código de ética, estatutos e informes (art. 5.10.23 de la Circular Única).'),
            dict(codigo='sanciones', etapa='Control', regimenes='todos', periodicidad_meses=None,
                 nombre='Régimen de sanciones internas documentado',
                 descripcion='Incorporado al reglamento interno de trabajo o al código de ética.'),
            dict(codigo='reporte_supersociedades', etapa='Reporte', regimenes='todos', periodicidad_meses=None,
                 nombre='Procedimiento de reporte de soborno transnacional a la Supersociedades',
                 descripcion='Art. 5.10.27 de la Circular Única, en los términos de la Ley 1778 de 2016.'),
        ],
        'reportes': [],
    },

    'sagrilaft': {
        'nombre': 'SAGRILAFT',
        'nombre_largo': 'Sistema de autocontrol y gestión del riesgo integral LA/FT/FPADM (Supersociedades)',
        'autoridad': 'Superintendencia de Sociedades',
        'icono': 'fa-building-shield',
        'resumen': 'Para sociedades vigiladas o supervisadas por la Supersociedades que superan los umbrales de ingresos o '
                   'activos de su sector. Debe actualizarse al menos cada dos años.',
        'a_quien_aplica': 'Empresas supervisadas por la Supersociedades con ingresos o activos iguales o superiores a '
                          '30.000 SMLMV (varios sectores; otros tienen umbrales propios) o con aportes en criptoactivos. '
                          'Las obligadas desde 2024 debían actualizarlo en 2026.',
        'normas': [
            ('Circular Externa 100-000016 de 2020 de la Supersociedades (cap. X CBJ), modificada por la 100-000004 de 2021', False),
            ('Circular Externa 100-300000 de 2024 (numerales 4.4 y 4.5)', False),
            ('Circular Básica Jurídica 100-000002 de 2025', False),
        ],
        'regimenes': {'completo': 'SAGRILAFT', 'minimo': 'Régimen de medidas mínimas'},
        'requisitos': [
            dict(codigo='politica', etapa='Diseño', regimenes='todos', periodicidad_meses=24,
                 nombre='Política LA/FT/FPADM aprobada por la junta o asamblea', descripcion='Evidencia: acta. Actualización al menos cada dos años.'),
            dict(codigo='manual', etapa='Diseño', regimenes=('completo',), periodicidad_meses=24,
                 nombre='Manual SAGRILAFT con procedimientos', descripcion='Identificación, medición, control y monitoreo; debida diligencia y debida diligencia intensificada.'),
            dict(codigo='oficial', etapa='Diseño', regimenes=('completo',), periodicidad_meses=None,
                 nombre='Oficial de cumplimiento designado y registrado en SIREL', descripcion='Acta, hoja de vida, independencia; registro en la UIAF.'),
            dict(codigo='matriz', etapa='Identificación', regimenes='todos', periodicidad_meses=12,
                 nombre='Matriz de riesgos LA/FT/FPADM', descripcion='Se gestiona en Riesgos.'),
            dict(codigo='debida_diligencia', etapa='Control', regimenes='todos', periodicidad_meses=None,
                 nombre='Conocimiento de contrapartes y beneficiario final', descripcion='Incluye la consulta de listas vinculantes y la identificación del beneficiario final (RUB). Se opera en Contrapartes.'),
            dict(codigo='ros', etapa='Reporte', regimenes='todos', periodicidad_meses=None,
                 nombre='Procedimiento de ROS y reportes a la UIAF', descripcion='Quién decide, plazos y soporte.'),
            dict(codigo='capacitacion', etapa='Operación', regimenes='todos', periodicidad_meses=12,
                 nombre='Capacitación anual', descripcion='Plan, asistencia y evaluación.'),
            dict(codigo='auditoria', etapa='Monitoreo', regimenes=('completo',), periodicidad_meses=12,
                 nombre='Evaluación del sistema por revisoría fiscal o auditoría', descripcion='Informe anual.'),
            dict(codigo='actualizacion_bienal', etapa='Monitoreo', regimenes='todos', periodicidad_meses=24,
                 nombre='Actualización bienal del sistema', descripcion='Revisión de política, manual y matriz al menos cada dos años.'),
        ],
        'reportes': [],
    },

    'datos_personales': {
        'nombre': 'Datos personales',
        'nombre_largo': 'Programa integral de gestión de datos personales (Ley 1581 de 2012) y Registro Nacional de Bases de Datos',
        'autoridad': 'Superintendencia de Industria y Comercio',
        'icono': 'fa-user-shield',
        'resumen': 'Toda empresa que trata datos de empleados, clientes o proveedores necesita política de tratamiento, '
                   'autorizaciones, aviso de privacidad y un responsable. Las de mayores activos además inscriben y '
                   'actualizan sus bases de datos en el RNBD.',
        'a_quien_aplica': 'Todas las empresas (programa documental). La inscripción en el RNBD aplica a sociedades y '
                          'entidades sin ánimo de lucro con activos totales superiores a 100.000 UVT y a las entidades públicas.',
        'normas': [
            ('Ley 1581 de 2012 y Decreto 1377 de 2013 (compilado en el Decreto 1074 de 2015)', False),
            ('Decreto 090 de 2018 (obligados al RNBD)', False),
            ('Circular Única de la SIC, título V, y Manual de usuario del RNBD', False),
        ],
        'regimenes': {'rnbd': 'Con inscripción en el RNBD', 'documental': 'Solo programa documental (sin RNBD)'},
        'requisitos': [
            dict(codigo='politica', etapa='Diseño', regimenes='todos', periodicidad_meses=None,
                 nombre='Política de tratamiento de datos personales publicada', descripcion='Finalidades, derechos del titular, canales de atención y procedimientos. Evidencia: documento y publicación.'),
            dict(codigo='aviso', etapa='Diseño', regimenes='todos', periodicidad_meses=None,
                 nombre='Aviso de privacidad', descripcion='En formularios, página web y puntos de recolección.'),
            dict(codigo='autorizaciones', etapa='Control', regimenes='todos', periodicidad_meses=None,
                 nombre='Autorizaciones de los titulares con prueba', descripcion='Empleados, clientes, proveedores y aspirantes; autorización separada para datos sensibles y de menores.'),
            dict(codigo='responsable', etapa='Diseño', regimenes='todos', periodicidad_meses=None,
                 nombre='Oficial o área responsable de protección de datos', descripcion='Quién atiende consultas y reclamos y rinde cuentas.'),
            dict(codigo='consultas_reclamos', etapa='Control', regimenes='todos', periodicidad_meses=None,
                 nombre='Procedimiento de consultas y reclamos con plazos', descripcion='Consultas en diez días hábiles y reclamos en quince días hábiles (arts. 14 y 15 de la Ley 1581), con registro de cada caso.'),
            dict(codigo='inventario', etapa='Identificación', regimenes='todos', periodicidad_meses=12,
                 nombre='Inventario de bases de datos y de encargados', descripcion='Qué bases existen, qué datos tienen, finalidad, encargados y transferencias.'),
            dict(codigo='seguridad', etapa='Control', regimenes='todos', periodicidad_meses=12,
                 nombre='Medidas de seguridad documentadas', descripcion='Accesos, copias, cifrado y contratos de transmisión con encargados.'),
            dict(codigo='incidentes', etapa='Control', regimenes='todos', periodicidad_meses=None,
                 nombre='Procedimiento de incidentes de seguridad', descripcion='Registro y reporte a la SIC en el RNBD dentro del plazo que fija la Circular.'),
            dict(codigo='rnbd_inscripcion', etapa='Reporte', regimenes=('rnbd',), periodicidad_meses=None,
                 nombre='Bases de datos inscritas en el RNBD', descripcion='Cada base nueva se inscribe dentro de los dos meses siguientes a su creación.'),
            dict(codigo='capacitacion', etapa='Operación', regimenes='todos', periodicidad_meses=12,
                 nombre='Capacitación anual al personal que trata datos', descripcion='Asistencia y material.'),
        ],
        'reportes': [
            dict(codigo='rnbd_actualizacion', nombre='Actualización anual del RNBD', fechas=[(3, 31)],
                 norma='Circular Única SIC (ventana del 2 de enero al 31 de marzo)', verificado=False),
            dict(codigo='rnbd_reclamos', nombre='Reporte semestral de reclamos en el RNBD', fechas=[(2, 20), (8, 25)],
                 norma='Circular Única SIC; la fecha exacta la fija la SIC cada año (2026: 20-feb y 25-ago)', verificado=False),
        ],
    },
}

ETAPAS = ('Diseño', 'Identificación', 'Control', 'Operación', 'Reporte', 'Monitoreo')
TIPOS_CONTRAPARTE = ('cliente', 'proveedor', 'empleado', 'socio', 'conductor', 'propietario_vehiculo', 'otro')
FACTORES_RIESGO = ('contraparte', 'producto', 'canal', 'jurisdiccion', 'proceso')


def requisitos_de(codigo_programa, regimen):
    """Requisitos del catálogo que aplican a un régimen."""
    prog = PROGRAMAS[codigo_programa]
    salida = []
    for r in prog['requisitos']:
        aplica = r['regimenes'] == 'todos' or regimen in r['regimenes']
        if aplica:
            salida.append(r)
    return salida


def requisito_info(codigo_programa, codigo_requisito):
    for r in PROGRAMAS[codigo_programa]['requisitos']:
        if r['codigo'] == codigo_requisito:
            return r
    return {'codigo': codigo_requisito, 'nombre': codigo_requisito, 'descripcion': '', 'etapa': '', 'periodicidad_meses': None}


def normas_pendientes(codigo_programa):
    return [c for c, v in PROGRAMAS[codigo_programa]['normas'] if not v]


# Integridad del catálogo al importar: códigos únicos y fechas válidas.
for _cod, _p in PROGRAMAS.items():
    _reqs = [r['codigo'] for r in _p['requisitos']]
    assert len(_reqs) == len(set(_reqs)), f'Requisitos repetidos en {_cod}'
    assert _p['regimenes'], f'{_cod} sin regímenes'
    for _r in _p['requisitos']:
        assert _r['etapa'] in ETAPAS, f'Etapa desconocida en {_cod}.{_r["codigo"]}'
        if _r['regimenes'] != 'todos':
            assert set(_r['regimenes']) <= set(_p['regimenes']), f'Régimen desconocido en {_cod}.{_r["codigo"]}'
    for _rep in _p['reportes']:
        for _m, _d in _rep['fechas']:
            assert 1 <= _m <= 12 and 1 <= _d <= 31, f'Fecha inválida en {_cod}.{_rep["codigo"]}'
