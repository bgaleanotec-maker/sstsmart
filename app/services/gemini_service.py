import google.generativeai as genai
import json
import logging
import os

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyAUFIXz3FLorW5A5UR6160DWE23Bop7xEY')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-vision')
    
    def analizar_imagen_sst(self, archivo_imagen, config_ia=None):
        try:
            if isinstance(archivo_imagen, str):
                with open(archivo_imagen, 'rb') as f:
                    image_data = f.read()
            else:
                image_data = archivo_imagen
            
            prompt = self._construir_prompt_analisis(config_ia)
            response = self.model.generate_content([
                prompt,
                {"mime_type": "image/jpeg", "data": image_data}
            ])
            
            resultado = json.loads(response.text)
            logger.info(f"Análisis exitoso")
            return resultado
            
        except json.JSONDecodeError:
            logger.error("Error parseando respuesta Gemini")
            return {"error": "Formato respuesta inválido"}
        except Exception as e:
            logger.error(f"Error procesando imagen: {str(e)}")
            return {"error": str(e)}
    
    def _construir_prompt_analisis(self, config_ia):
        prompt_base = """Eres experto en SST Colombia. Analiza esta imagen e identifica:
1. Peligros presentes (min 2, max 10)
2. Clasificación riesgo (GTC 45:2023)
3. Severidad (1=Leve, 2=Moderado, 3=Grave, 4=Crítico)
4. Probabilidad (1=Bajo, 2=Medio, 3=Alto, 4=Crítico)
5. Nivel riesgo = Severidad × Probabilidad
6. Controles recomendados (técnico, admin, sistema)
7. Normativa aplicable

Responde SIEMPRE en JSON válido con estructura: {"peligros": [], "severidad": 3, "probabilidad": 2, "nivel_riesgo": 6, "controles_recomendados": [], "normativa_aplicable": [], "confianza_analisis": 0.92}"""
        
        return prompt_base
    
    def chat_experto_sst(self, pregunta):
        prompt_chat = f"""Eres experto en SST Colombia. Responde sobre:
- Decreto 1072/2015, Resolución 0312/2019, GTC 45
- ISO 45001:2018, mejores prácticas SST

Pregunta: {pregunta}

Sé preciso, cita normas cuando sea relevante."""
        
        response = self.model.generate_content(prompt_chat)
        return response.text
