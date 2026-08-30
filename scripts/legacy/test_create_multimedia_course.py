from app import create_app, db
from app import create_app, db
from app.models import Usuario
from app.models.formacion import Curso
from flask_login import login_user
from flask_login import login_user

app = create_app()

def test_create_course():
    with app.app_context():
        # 1. Setup Admin User
        admin = Usuario.query.filter_by(email='admin@sst.com').first()
        if not admin:
            # Create dummy admin if not exists (likely exists)
            print("⚠️ Admin not found, checking generic admin")
            admin = Usuario.query.filter_by(rol='Admin').first()
        
        if not admin:
            print("❌ No admin user found to test with.")
            # Create temp admin
            admin = Usuario(email='testadmin@test.com', nombre='Test', apellido='Admin', rol='Admin')
            admin.set_password('1234')
            db.session.add(admin)
            db.session.commit()
            print("✅ Created temp admin")

        # 2. Test Client
        with app.test_client() as client:
            # Login
            with client.session_transaction() as sess:
                sess['_user_id'] = str(admin.id)
                sess['_fresh'] = True
            
            # 3. Send POST Request with new fields
            print("🚀 Sending POST to /admin/formacion/curso/nuevo")
            response = client.post('/admin/formacion/curso/nuevo', data={
                'titulo': 'Curso Test Python Script',
                'categoria': 'Seguridad Industrial',
                'duracion_horas': '2',
                'tipo_contenido': 'video',
                'video_url': 'https://youtube.com/test',
                'imagen_portada': 'https://img.com/1',
                'descripcion': 'Test description',
                'contenido_html': '<p>Hola</p>'
            }, follow_redirects=True)
            
            if response.status_code == 200:
                # Check for success message in HTML
                if b'Curso creado exitosamente' in response.data:
                    print("✅ SUCCESS: Curso created.")
                else:
                    print(f"⚠️ Response 200 but success message missing. Possible validation error form re-render?")
                    # Print part of body to see errors
                    print(response.data[:500])
            else:
                 print(f"❌ FAILED with status: {response.status_code}")
                 print(response.data)

            # 4. Verify DB
            curso = Curso.query.filter_by(titulo='Curso Test Python Script').first()
            if curso:
                print(f"✅ DB Verify: Found course ID {curso.id}, cat={curso.categoria}")
                # Cleanup
                db.session.delete(curso)
                db.session.commit()
            else:
                print("❌ DB Verify: Course NOT found in DB.")

if __name__ == "__main__":
    test_create_course()
