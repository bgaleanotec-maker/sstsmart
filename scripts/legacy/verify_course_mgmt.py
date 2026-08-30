from app import create_app, db
from app.models.formacion import Curso, matriculas
from app.models.usuario import Usuario

app = create_app('development')

def verify_management():
    with app.app_context():
        print("🔍 Verificando Gestión de Cursos y Matrículas...")

        # 1. Setup Test Data
        admin = Usuario.query.filter_by(rol='Admin').first()
        if not admin:
            print("⚠️ No Admin found, creating dummy...")
            admin = Usuario(email='admin_test@sst.com', nombre_completo='Admin Test', rol='Admin')
            db.session.add(admin)
        
        user = Usuario.query.filter_by(email='student_test@sst.com').first()
        if not user:
            user = Usuario(email='student_test@sst.com', nombre_completo='Student Test', rol='Empleado')
            user.set_password('123')
            db.session.add(user)
        
        db.session.commit()

        # 2. Create Course
        curso = Curso(titulo="Curso Test Mgmt", descripcion="Test Management", estado="Activo")
        db.session.add(curso)
        db.session.commit()
        print(f"✅ Curso creado: {curso.id}")

        # 3. Test Enrollment (Matricula)
        print("Testing Enrollment...")
        curso.estudiantes.append(user)
        db.session.commit()
        
        # Verify
        check_curso = Curso.query.get(curso.id)
        if user in check_curso.estudiantes:
            print(f"✅ Usuario {user.nombre_completo} matriculado correctamente.")
        else:
            print("❌ Falló la matrícula.")

        # 4. Test Unenrollment
        print("Testing Unenrollment...")
        curso.estudiantes.remove(user)
        db.session.commit()
        
        if user not in check_curso.estudiantes:
            print("✅ Usuario desmatriculado correctamente.")
        else:
            print("❌ Falló la desmatrícula.")

        # 5. Test Toggle Status
        print("Testing Toggle Status...")
        curso.estado = 'Inactivo'
        db.session.commit()
        if curso.estado == 'Inactivo':
            print("✅ Estado cambiado a Inactivo.")
        else:
            print("❌ Falló cambio de estado.")

        # 6. Test Delete
        print("Testing Deletion...")
        cid = curso.id
        db.session.delete(curso)
        db.session.commit()
        
        deleted = Curso.query.get(cid)
        if not deleted:
            print("✅ Curso eliminado correctamente.")
        else:
            print("❌ Falló la eliminación.")

        # Cleanup User
        # db.session.delete(user)
        # db.session.commit()
        print("✅ Verificación completada.")

if __name__ == "__main__":
    verify_management()
