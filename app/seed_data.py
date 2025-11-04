"""
Script para cargar datos iniciales en SST Colombia
"""
from app import create_app, db
from app.models import Usuario, RolSST, RiesgoMatriz, Control
from app.models.control import TipoControl, NivelControl, EstadoControl
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def seed_database():
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("🌱 CARGA DE DATOS SST COLOMBIA")
        print("=" * 60)
        
        # Crear roles
        print("\n📋 Creando roles...")
        roles_data = [
            {'nombre': 'Admin', 'descripcion': 'Administrador'},
            {'nombre': 'Responsable SST', 'descripcion': 'Responsable SST'},
            {'nombre': 'Abogado', 'descripcion': 'Abogado'},
            {'nombre': 'Gerente Area', 'descripcion': 'Gerente'},
            {'nombre': 'Responsable Control', 'descripcion': 'Control'},
            {'nombre': 'Auditor', 'descripcion': 'Auditor'},
        ]
        
        roles = {}
        for rol_data in roles_data:
            rol = RolSST.query.filter_by(nombre=rol_data['nombre']).first()
            if not rol:
                rol = RolSST(**rol_data)
                db.session.add(rol)
            roles[rol_data['nombre']] = rol
        
        db.session.commit()
        
        # Crear usuarios
        print("👥 Creando usuarios...")
        usuarios_data = [
            {'nombre_completo': 'Admin SST', 'email': 'admin@sst.local', 'contraseña': 'admin123', 'rol': 'Admin'},
            {'nombre_completo': 'Responsable SST', 'email': 'sst@sst.local', 'contraseña': 'sst123', 'rol': 'Responsable SST'},
            {'nombre_completo': 'Abogado', 'email': 'abogado@sst.local', 'contraseña': 'abogado123', 'rol': 'Abogado'},
            {'nombre_completo': 'Gerente', 'email': 'gerente@sst.local', 'contraseña': 'gerente123', 'rol': 'Gerente Area'},
            {'nombre_completo': 'Juan Control', 'email': 'juan@sst.local', 'contraseña': 'juan123', 'rol': 'Responsable Control'},
            {'nombre_completo': 'María Auditor', 'email': 'maria@sst.local', 'contraseña': 'maria123', 'rol': 'Auditor'},
        ]
        
        usuarios = {}
        for user_data in usuarios_data:
            usuario = Usuario.query.filter_by(email=user_data['email']).first()
            if not usuario:
                usuario = Usuario(
                    nombre_completo=user_data['nombre_completo'],
                    email=user_data['email'],
                    contraseña_hash=generate_password_hash(user_data['contraseña']),
                    rol=user_data['rol'],
                    activo=True
                )
                db.session.add(usuario)
            usuarios[user_data['email']] = usuario
        
        db.session.commit()
        
        # Crear riesgos
        print("⚠️ Creando riesgos...")
        riesgos_data = [
            {'nombre_riesgo': 'Caída desde altura', 'descripcion': 'Caída de trabajadores', 'probabilidad': 3, 'severidad': 3},
            {'nombre_riesgo': 'Atrapamiento', 'descripcion': 'Atrapamiento en máquinas', 'probabilidad': 2, 'severidad': 4},
            {'nombre_riesgo': 'Químicos', 'descripcion': 'Exposición a químicos', 'probabilidad': 3, 'severidad': 3},
            {'nombre_riesgo': 'Ruido', 'descripcion': 'Ruido excesivo', 'probabilidad': 4, 'severidad': 2},
            {'nombre_riesgo': 'Carga manual', 'descripcion': 'Levantamiento manual', 'probabilidad': 4, 'severidad': 2},
        ]
        
        riesgos = {}
        for riesgo_data in riesgos_data:
            riesgo = RiesgoMatriz.query.filter_by(nombre_riesgo=riesgo_data['nombre_riesgo']).first()
            if not riesgo:
                riesgo = RiesgoMatriz(**riesgo_data, activo=True)
                riesgo.clasificacion = riesgo.probabilidad * riesgo.severidad
                db.session.add(riesgo)
            riesgos[riesgo_data['nombre_riesgo']] = riesgo
        
        db.session.commit()
        
        # Crear controles
        print("🛡️ Creando controles...")
        controles_data = [
            {'nombre': 'Implementar arnés', 'tipo': TipoControl.PREVENTIVO.value, 'nivel': NivelControl.INDIVIDUO.value, 'riesgo': 'Caída desde altura', 'responsable': 'juan@sst.local', 'estado': EstadoControl.IMPLEMENTADO.value, 'efectividad': 95},
            {'nombre': 'Colocar guardias', 'tipo': TipoControl.PREVENTIVO.value, 'nivel': NivelControl.FUENTE.value, 'riesgo': 'Atrapamiento', 'responsable': 'gerente@sst.local', 'estado': EstadoControl.EN_PROCESO.value, 'efectividad': 0},
            {'nombre': 'Capacitación químicos', 'tipo': TipoControl.CORRECTIVO.value, 'nivel': NivelControl.ADMINISTRATIVO.value, 'riesgo': 'Químicos', 'responsable': 'sst@sst.local', 'estado': EstadoControl.VERIFICADO.value, 'efectividad': 88},
            {'nombre': 'Protección auditiva', 'tipo': TipoControl.PREVENTIVO.value, 'nivel': NivelControl.INDIVIDUO.value, 'riesgo': 'Ruido', 'responsable': 'juan@sst.local', 'estado': EstadoControl.EFECTIVO.value, 'efectividad': 92},
            {'nombre': 'Levantamiento seguro', 'tipo': TipoControl.CORRECTIVO.value, 'nivel': NivelControl.ADMINISTRATIVO.value, 'riesgo': 'Carga manual', 'responsable': 'maria@sst.local', 'estado': EstadoControl.PLANIFICADO.value, 'efectividad': 0},
        ]
        
        for idx, control_data in enumerate(controles_data, start=1):
            codigo = f"CTL-{idx:03d}-{datetime.now().year}"
            control = Control.query.filter_by(codigo=codigo).first()
            
            if not control:
                riesgo = riesgos.get(control_data['riesgo'])
                responsable = usuarios.get(control_data['responsable'])
                
                if riesgo and responsable:
                    control = Control(
                        codigo=codigo,
                        nombre=control_data['nombre'],
                        tipo_control=control_data['tipo'],
                        nivel_control=control_data['nivel'],
                        riesgo_id=riesgo.id,
                        responsable_id=responsable.id,
                        creado_por=usuarios['admin@sst.local'].id,
                        creado_por_rol='Admin',
                        estado=control_data['estado'],
                        efectividad_porcentaje=control_data['efectividad'],
                        fecha_planeada=datetime.now() + timedelta(days=15),
                        requiere_seguimiento_periodico=True,
                        frecuencia_seguimiento_dias=30,
                        activo=True
                    )
                    db.session.add(control)
        
        db.session.commit()
        
        print("\n✅ DATOS CARGADOS")
        print("=" * 60)
        print("Usuarios:")
        for user_data in usuarios_data:
            print(f"  {user_data['email']} / {user_data['contraseña']}")

if __name__ == '__main__':
    seed_database()