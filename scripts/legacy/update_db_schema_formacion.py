from app import create_app, db
from sqlalchemy import text

app = create_app()

def update_schema():
    with app.app_context():
        # SQLite doesn't support adding multiple columns in one statement reliably in all versions, 
        # so we add them one by one.
        
        # Columns to add
        new_columns = [
            ("tipo_contenido", "VARCHAR(20) DEFAULT 'video'"),
            ("categoria", "VARCHAR(100) DEFAULT 'General'"),
            ("imagen_portada", "VARCHAR(500)"),
            ("pdf_url", "VARCHAR(500)")
        ]
        
        with db.engine.connect() as conn:
            for col_name, col_type in new_columns:
                try:
                    # Check if column exists is hard in raw SQL without querying schema extensively, 
                    # easier to try adding and ignore duplicate error or handle it.
                    # Or check schema first.
                    
                    # Simple check:
                    check_sql = text(f"SELECT {col_name} FROM cursos LIMIT 1")
                    try:
                        conn.execute(check_sql)
                        print(f"✅ Column {col_name} already exists.")
                    except Exception:
                        # Column doesn't exist, add it
                        print(f"➕ Adding column {col_name}...")
                        alter_sql = text(f"ALTER TABLE cursos ADD COLUMN {col_name} {col_type}")
                        conn.execute(alter_sql)
                        print(f"✅ Fixed {col_name}.")
                        
                except Exception as e:
                    print(f"❌ Error checking/adding {col_name}: {e}")
            
            conn.commit()
            print("🎉 Schema update complete.")

if __name__ == "__main__":
    update_schema()
