"""Integración con Google Gemini para análisis SST.

La API key viene SOLO de configuración (env GEMINI_API_KEY o ConfiguracionIA);
nunca debe incrustarse en el código. El modelo es configurable vía env
GEMINI_MODEL (default gemini-2.0-flash).
"""
import json
import logging
import os

import requests

logger = logging.getLogger(__name__)

_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


class GeminiService:
    def __init__(self, api_key=None, model=None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = model or os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY no configurada. Defínela en el entorno o en "
                "Configuración de IA."
            )

    def _generate(self, parts):
        url = f"{_API_BASE}/{self.model}:generateContent"
        resp = requests.post(
            url,
            headers={"x-goog-api-key": self.api_key,
                     "Content-Type": "application/json"},
            json={"contents": [{"parts": parts}]},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    def analizar_imagen_sst(self, archivo_imagen, config_ia=None):
        """Analiza una imagen de condición insegura. Devuelve dict."""
        import base64
        try:
            if isinstance(archivo_imagen, str):
                with open(archivo_imagen, 'rb') as f:
                    image_data = f.read()
            else:
                image_data = archivo_imagen

            prompt = self._construir_prompt_analisis(config_ia)
            texto = self._generate([
                {"text": prompt},
                {"inline_data": {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(image_data).decode(),
                }},
            ])
            # El modelo puede envolver el JSON en ```json ... ```
            texto = texto.strip()
            if texto.startswith('```'):
                texto = texto.strip('`')
                texto = texto[texto.find('{'):texto.rfind('}') + 1]
            return json.loads(texto)

        except json.JSONDecodeError:
            logger.error("Respuesta de Gemini no es JSON válido")
            return {"error": "Formato respuesta inválido"}
        except Exception as e:
            logger.error(f"Error procesando imagen: {e}")
            return {"error": str(e)}

    def _construir_prompt_analisis(self, config_ia=None):
        if config_ia is not None and getattr(config_ia, 'prompt_sistema', None):
            return config_ia.prompt_sistema
        return """Eres experto en SST Colombia. Analiza esta imagen e identifica:
1. Peligros presentes (min 2, max 10)
2. Clasificación riesgo (GTC 45)
3. Severidad (1=Leve, 2=Moderado, 3=Grave, 4=Crítico)
4. Probabilidad (1=Bajo, 2=Medio, 3=Alto, 4=Crítico)
5. Nivel riesgo = Severidad × Probabilidad
6. Controles recomendados (técnico, admin, sistema)
7. Normativa aplicable

Responde SIEMPRE con JSON válido y nada más: {"peligros": [], "severidad": 3, "probabilidad": 2, "nivel_riesgo": 6, "controles_recomendados": [], "normativa_aplicable": [], "confianza_analisis": 0.92}"""

    def chat_experto_sst(self, pregunta):
        prompt_chat = f"""Eres experto en SST Colombia (SG-SST). Marco normativo vigente:
- Ley 1562/2012, Decreto 1072/2015 (cap. 2.2.4.6), Resolución 0312/2019 (estándares mínimos)
- Riesgo psicosocial: Resolución 2764/2022 (derogó la 2404/2019)
- Exámenes médicos ocupacionales: Resolución 1843/2025 (derogó la 2346/2007)
- Comités de convivencia: Resolución 3461/2025 (derogó 652 y 1356 de 2012)
- Alturas: Resolución 4272/2021. Reporte AT/EL: Resolución 156/2005 + 2851/2015
- Reforma laboral: Ley 2466/2025. GTC 45 e ISO 45001:2018 como guías.

Pregunta: {pregunta}

Sé preciso, cita normas cuando sea relevante y aclara cuando algo requiera validación de un abogado laboral."""
        return self._generate([{"text": prompt_chat}])
