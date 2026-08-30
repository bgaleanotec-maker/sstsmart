"""Constantes de dominio: roles y grupos de permiso.

Único punto de verdad para los nombres de rol. El código antiguo mezclaba
'Responsable SST', 'Responsable_SST' y 'ResponsableSST'; las comparaciones
deben hacerse SIEMPRE vía Usuario.tiene_rol(), que normaliza.
"""

# Roles canónicos (valor guardado en usuarios.rol para cuentas nuevas)
ROL_ADMIN = 'Admin'
ROL_RESPONSABLE_SST = 'Responsable_SST'
ROL_ABOGADO = 'Abogado'
ROL_GERENTE = 'Gerente'
ROL_AUDITOR = 'Auditor'
ROL_EMPLEADO = 'Empleado'
ROL_CONTRATISTA = 'Contratista'

ROLES_TODOS = [
    ROL_ADMIN, ROL_RESPONSABLE_SST, ROL_ABOGADO, ROL_GERENTE,
    ROL_AUDITOR, ROL_EMPLEADO, ROL_CONTRATISTA,
]

# Grupos de permiso
ROLES_GESTION = (ROL_ADMIN, ROL_RESPONSABLE_SST, ROL_ABOGADO)
ROLES_GESTION_CONTROLES = (ROL_ADMIN, ROL_RESPONSABLE_SST, ROL_ABOGADO, ROL_GERENTE)
ROLES_VERIFICACION = (ROL_ADMIN, ROL_RESPONSABLE_SST, ROL_ABOGADO, ROL_AUDITOR)
ROLES_JURIDICO = (ROL_ADMIN, ROL_RESPONSABLE_SST, ROL_ABOGADO)
ROLES_RESOLVER_JURIDICO = (ROL_ADMIN, ROL_ABOGADO)
ROLES_FORMACION_ADMIN = (ROL_ADMIN, ROL_RESPONSABLE_SST)


def normalizar_rol(rol):
    """'Responsable SST' / 'ResponsableSST' / 'responsable_sst' -> 'responsablesst'."""
    if not rol:
        return ''
    return rol.replace(' ', '').replace('_', '').replace('-', '').lower()
