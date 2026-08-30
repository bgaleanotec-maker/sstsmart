
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Usuario, Curso, Examen, Pregunta, Opcion, IntentoExamen, ProgresoFormacion
from app.routes.formacion import calcular_ranking_sst

def verify_formation_score():
    """
    Verifies the entire formation flow:
    1. Create a Course & Exam.
    2. Create a User.
    3. User takes exam -> Pass.
    4. Check Score Calculation (should be 100%).
    """
    app = create_app()
    with app.app_context():
        print("🚀 Verifying Formation Module Scoring...")
        
        # 0. Setup: Clean previous test data (optional, but good for idempotency)
        # For simplicity, we create unique data
        
        # 1. Create a User
        test_email = "student@test.com"
        user = Usuario.query.filter_by(email=test_email).first()
        if not user:
            user = Usuario(email=test_email, nombre_completo="Test Student", rol="Empleado", contraseña_hash="hash")
            db.session.add(user)
            db.session.commit()
            print(f"✅ Created Test User: {user.email}")
        else:
             print(f"ℹ️ User already exists: {user.email}")
        
        # 2. Create Course & Exam
        course_title = "Curso Basico SST"
        curso = Curso.query.filter_by(titulo=course_title).first()
        if not curso:
            curso = Curso(titulo=course_title, descripcion="Intro", estado='Activo')
            db.session.add(curso)
            db.session.flush()
            
            examen = Examen(titulo="Examen Final", curso_id=curso.id, porcentaje_aprobacion=50, puntaje_total=10)
            db.session.add(examen)
            db.session.flush()
            
            pregunta = Pregunta(examen_id=examen.id, texto_pregunta="¿SST?", puntaje=10)
            db.session.add(pregunta)
            db.session.flush()
            
            opcion = Opcion(pregunta_id=pregunta.id, texto_opcion="Si", es_correcta=True)
            db.session.add(opcion)
            db.session.commit()
            print(f"✅ Created Course & Exam: {curso.titulo}")
        else:
            examen = Examen.query.filter_by(curso_id=curso.id).first()
            print(f"ℹ️ Course already exists: {curso.titulo}")
            
        # 3. Check Initial Score (Should be 0 if no exams passed)
        initial_score = calcular_ranking_sst(user.id)
        print(f"📊 Initial Score: {initial_score} (Expected: Low or 0)")
        
        # 4. Simulate Passing Exam
        # Clear previous attempts
        IntentoExamen.query.filter_by(usuario_id=user.id).delete()
        db.session.commit()
        
        print("📝 Taking Exam (Simulated)...")
        intento = IntentoExamen(
            usuario_id=user.id,
            examen_id=examen.id,
            puntaje_obtenido=10, # Max score
            aprobado=True
        )
        db.session.add(intento)
        db.session.commit()
        
        # 5. Check New Score
        # We assume this user is assigned all active courses. 
        # If there is only 1 active course in DB and they passed 1, score should be 100.
        # But if there are other courses in DB (seeded), score might be lower.
        
        total_active_courses = Curso.query.filter_by(estado='Activo').count()
        print(f"ℹ️ Total Active Courses in DB: {total_active_courses}")
        
        new_score = calcular_ranking_sst(user.id)
        print(f"📊 New Score: {new_score}")
        
        expected_score = (1 / total_active_courses) * 100
        print(f"ℹ️ Expected Score calculation: (1 / {total_active_courses}) * 100 = {expected_score}")
        
        if new_score == expected_score:
            print("✅ Score calculation is CORRECT.")
        else:
            # Floating point comparison might need tolerance, but simple check is okay
            if abs(new_score - expected_score) < 0.1:
                 print("✅ Score calculation is CORRECT (Approx).")
            else:
                 print("❌ Score calculation mismatch.")
                 
        return True

if __name__ == "__main__":
    verify_formation_score()
