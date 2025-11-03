from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()

def iniciar_scheduler(app):
    """Inicia el scheduler con tareas periódicas"""
    
    with app.app_context():
        # Tarea 1: Verificar vencimientos cada 5 minutos
        scheduler.add_job(
            func=verificar_vencimientos_task,
            trigger=IntervalTrigger(minutes=5),
            id='verificar_vencimientos',
            name='Verificar vencimientos de respuesta/resolución',
            replace_existing=True,
            args=[app]
        )
        
        # Tarea 2: Limpiar tareas completadas cada 1 hora
        scheduler.add_job(
            func=limpiar_tareas_completadas_task,
            trigger=IntervalTrigger(hours=1),
            id='limpiar_tareas',
            name='Limpiar tareas completadas',
            replace_existing=True,
            args=[app]
        )
        
        if not scheduler.running:
            scheduler.start()
            logger.info("✅ Scheduler iniciado correctamente")
        else:
            logger.info("ℹ️ Scheduler ya está corriendo")

def verificar_vencimientos_task(app):
    """
    Tarea periódica que verifica qué reportes se vencieron
    y ejecuta el escalonamiento automático
    """
    with app.app_context():
        try:
            from app.services.gestion_reportes_service import GestionReportesService
            
            escalados = GestionReportesService.verificar_vencimientos()
            
            if escalados > 0:
                logger.info(f"✅ {escalados} reportes escalonados automáticamente")
            
        except Exception as e:
            logger.error(f"❌ Error en verificar_vencimientos_task: {str(e)}", exc_info=True)

def limpiar_tareas_completadas_task(app):
    """
    Tarea de mantenimiento que limpia tareas antiguas completadas
    """
    with app.app_context():
        try:
            from app.models import TareaGestion
            from app import db
            from datetime import datetime, timedelta
            
            # Eliminar tareas completadas hace más de 30 días
            fecha_limite = datetime.utcnow() - timedelta(days=30)
            
            tareas_eliminadas = TareaGestion.query.filter(
                TareaGestion.estado == 'Completada',
                TareaGestion.fecha_completada < fecha_limite
            ).delete()
            
            db.session.commit()
            
            if tareas_eliminadas > 0:
                logger.info(f"🧹 {tareas_eliminadas} tareas antiguas eliminadas")
            
        except Exception as e:
            logger.error(f"❌ Error en limpiar_tareas_completadas_task: {str(e)}", exc_info=True)

# Función para ejecutar regla manualmente (útil para debugging)
def ejecutar_regla_manual(app, gestion_id):
    """Ejecuta el escalonamiento de un reporte manualmente"""
    with app.app_context():
        try:
            from app.services.gestion_reportes_service import GestionReportesService
            
            result = GestionReportesService.escalonar_automatico(gestion_id)
            
            if result:
                logger.info(f"✅ Regla ejecutada manualmente para gestion_id={gestion_id}")
                return True
            else:
                logger.warning(f"⚠️ No se pudo ejecutar regla para gestion_id={gestion_id}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error ejecutando regla manual: {str(e)}", exc_info=True)
            return False