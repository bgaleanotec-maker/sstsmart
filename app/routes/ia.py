from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import ConfiguracionIA
from app.services.gemini_service import GeminiService
from app.routes import ia_bp

@ia_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.get_json()
    pregunta = data.get('pregunta', '')
    
    config_ia = ConfiguracionIA.query.filter_by(activo=True).first()
    if not config_ia:
        return jsonify({"error": "IA no configurada"}), 400
    
    try:
        gemini = GeminiService()
        respuesta = gemini.chat_experto_sst(pregunta)
        return jsonify({"respuesta": respuesta}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ia_bp.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    if current_user.rol != 'Admin':
        return jsonify({"error": "No autorizado"}), 403
    
    if request.method == 'POST':
        config = ConfiguracionIA.query.first() or ConfiguracionIA()
        config.nombre_modelo = request.form.get('nombre_modelo')
        config.prompt_sistema = request.form.get('prompt_sistema')
        config.umbral_confianza = float(request.form.get('umbral_confianza', 0.75))
        config.activo = True
        
        db.session.add(config)
        db.session.commit()
        return jsonify({"success": True}), 200
    
    config = ConfiguracionIA.query.first()
    return render_template('configuracion/ia.html', config=config)
