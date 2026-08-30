from app import create_app, db
from app.models.matriz_legal import RequisitoLegal, ValoracionJuridica, LogMatrizLegal, EstadoRequisito, ProbabilidadSancion
from app.models.usuario import Usuario
from flask import url_for

app = create_app('development')

def test_legal_matrix():
    with app.app_context():
        print("🔍 Iniciando Test Forense de Matriz Legal...")
        
        # 1. Setup User (Abogado)
        abogado = Usuario.query.filter_by(email='abogado_test@sst.com').first()
        if not abogado:
            abogado = Usuario(nombre_completo='Abogado Test', email='abogado_test@sst.com', rol='Juridico')
            abogado.set_password('123456')
            db.session.add(abogado)
            db.session.commit()
            print(f"✅ Usuario Jurídico creado/encontrado: {abogado.id}")

        # 2. Create Requisito (Norma)
        req = RequisitoLegal(
            norma="Resolución Test 001",
            articulo="Art. 5",
            descripcion="Prueba de lógica de riesgo",
            entidad="MinTest",
            anio=2026,
            estado=EstadoRequisito.PENDIENTE
        )
        db.session.add(req)
        db.session.commit()
        
        req.log_accion(abogado.id, "CREACION", "Creación automática por test")
        db.session.commit()
        print(f"✅ Requisito creado: ID {req.id}")

        # 3. Create Valoracion (High Risk)
        # Prob = ALTA (3), Impacto = 5,000,000 -> Riesgo = 15,000,000
        val_high = ValoracionJuridica(
            requisito_id=req.id,
            usuario_id=abogado.id,
            puntuacion_cumplimiento=10,
            probabilidad_sancion=ProbabilidadSancion.ALTA, # 3
            impacto_financiero=5000000.0,
            concepto_final="Concepto de riesgo alto por test"
        )
        db.session.add(val_high)
        db.session.commit()
        
        # Test Calculation
        riesgo = val_high.nivel_riesgo_total
        print(f"📊 Riesgo Calculado: {riesgo} (Esperado: 15,000,000)")
        
        # Test Semaforo
        semaforo = val_high.color_semaforo
        print(f"🚦 Semáforo: {semaforo} (Esperado: red)")
        
        if riesgo == 15000000.0 and semaforo == 'red':
            print("✅ Lógica de Riesgo Alto: CORRECTA")
        else:
            print("❌ Lógica de Riesgo Alto: FALLÓ")

        # 4. Create Valoracion (Low Risk)
        # Prob = BAJA (1), Impacto = 100,000 -> Riesgo = 100,000
        val_low = ValoracionJuridica(
            requisito_id=req.id,
            usuario_id=abogado.id,
            puntuacion_cumplimiento=90,
            probabilidad_sancion=ProbabilidadSancion.BAJA, # 1
            impacto_financiero=100000.0,
            concepto_final="Concepto bajo riesgo"
        )
        db.session.add(val_low)
        db.session.commit()
        
        semaforo_low = val_low.color_semaforo
        print(f"🚦 Semáforo (Bajo): {semaforo_low} (Esperado: green)")

        # 5. Check Logs
        logs = LogMatrizLegal.query.filter_by(requisito_id=req.id).all()
        print(f"📜 Logs Forenses encontrados: {len(logs)}")
        for log in logs:
            print(f"   - {log.timestamp}: {log.accion} - {log.detalles}")
            
        if len(logs) >= 1:
             print("✅ Auditoría Forense: FUNCIONANDO")
        else:
             print("❌ Auditoría Forense: FALLÓ")

        # Clean up
        print("🧹 Limpiando datos de prueba...")
        db.session.delete(val_high)
        db.session.delete(val_low)
        for l in logs: db.session.delete(l)
        db.session.delete(req)
        # db.session.delete(abogado) # Keep user for future tests
        db.session.commit()
        print("✅ Finalizado.")

if __name__ == "__main__":
    test_legal_matrix()
