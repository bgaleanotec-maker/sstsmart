
from app import create_app, db
from app.models import CondicionInsegura, TipoReporte

app = create_app()
with app.app_context():
    # Check if attributes exist on the class/instance
    print("Checking attributes on CondicionInsegura...")
    
    # Intanciate a dummy object (not saved to DB)
    ci = CondicionInsegura()
    
    try:
        # Just accessing them to see if they raise AttributeError
        print(f"Has tipo_reporte_obj? {hasattr(ci, 'tipo_reporte_obj')}")
        print(f"Has tipo_evidencia_obj? {hasattr(ci, 'tipo_evidencia_obj')}")
        print(f"Has ubicacion_incidente? {hasattr(ci, 'ubicacion_incidente')}")
        
        # Also check column existence
        print(f"Has tipo_reporte_id? {hasattr(ci, 'tipo_reporte_id')}")
        
        print("\n✅ Verification SUCCESS: Attributes are present.")
    except Exception as e:
        print(f"\n❌ Verification FAILED: {e}")
