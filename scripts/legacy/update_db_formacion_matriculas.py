from app import create_app, db
from app.models.formacion import matriculas
from sqlalchemy import inspect

app = create_app('development')

def update_schema():
    with app.app_context():
        inspector = inspect(db.engine)
        if 'matriculas' not in inspector.get_table_names():
            print("Creating table: matriculas")
            matriculas.create(db.engine)
            print("✅ Table created successfully.")
        else:
            print("Table 'matriculas' already exists.")

if __name__ == "__main__":
    update_schema()
