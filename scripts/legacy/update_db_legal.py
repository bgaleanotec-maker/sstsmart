from app import create_app, db
from app.models.matriz_legal import RequisitoLegal, ValoracionJuridica, EvidenciaLegal, LogMatrizLegal
from sqlalchemy import inspect

app = create_app('development')

def update_schema():
    with app.app_context():
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        tables_to_create = [
            'requisitos_legales',
            'valoraciones_juridicas',
            'evidencias_legales',
            'logs_matriz_legal'
        ]
        
        print("Checking tables...")
        created_count = 0
        for table in tables_to_create:
            if table not in existing_tables:
                print(f"Creating table: {table}")
                # This is a bit hacky but works for SQLite/Simple setups without migrations
                # In production, use `flask db migrate`
                try:
                    # Create specific model based on table name map
                    if table == 'requisitos_legales':
                        RequisitoLegal.__table__.create(db.engine)
                    elif table == 'valoraciones_juridicas':
                        ValoracionJuridica.__table__.create(db.engine)
                    elif table == 'evidencias_legales':
                        EvidenciaLegal.__table__.create(db.engine)
                    elif table == 'logs_matriz_legal':
                        LogMatrizLegal.__table__.create(db.engine)
                    
                    created_count += 1
                except Exception as e:
                    print(f"Error creating {table}: {e}")
            else:
                print(f"Table {table} already exists.")
                
        if created_count > 0:
            print(f"Successfully created {created_count} tables.")
        else:
            print("All tables already existed. No changes made.")

if __name__ == "__main__":
    update_schema()
