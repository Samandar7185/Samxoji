import google.generativeai as genai
from loguru import logger
import os
import json

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY topilmadi!")
            return
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        logger.success("✅ Gemini 1.5 Flash tayyor")

    async def correct_and_enrich_query(self, query: str):
        prompt = f"""
        Foydalanuvchi kino yoki anime qidirayapti: "{query}"
        
        Vazifang:
        1. Imlo xatolarini to'g'rilash
        2. Asl nomini aniqlash
        3. O'zbek, Rus, Ingliz variantlarini berish
        4. Kalit so'zlarni chiqarish
        
        JSON formatida qaytar:
        {{"corrected_query": "...", "english_title": "...", "uzbek_title": "...", "keywords": ["..."]}}
        """
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip().replace('```json', '').replace('```', '')
            return json.loads(text)
        except Exception as e:
            logger.error(f"Gemini xatosi: {e}")
            return {"corrected_query": query, "english_title": query, "keywords": query.split()}

gemini_service = GeminiService()
