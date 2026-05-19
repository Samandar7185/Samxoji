import google.generativeai as genai
from config.settings import settings
from database.database import get_db_connection # Bazaga ulanish

# Gemini API sozlamasi
genai.configure(api_key=settings.GEMINI_API_KEY)

async def get_embedding(text: str):
    """Matnni AI embedding (vektor) ko'rinishiga o'tkazish"""
    response = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document"
    )
    return response['embedding']

async def search_movies(query: str, limit: int = 5):
    """Kinolarni ma'nosiga qarab PgVector orqali qidirish"""
    query_vector = await get_embedding(query)
    
    conn = await get_db_connection()
    try:
        # PgVector yordamida eng yaqin vektorlarni topish (Cosine similarity)
        # Eslatma: Baza modellarida embedding ustuni 'embedding' deb nomlangan bo'lishi kerak
        rows = await conn.fetch(
            """
            SELECT id, title, file_id, caption 
            FROM movies 
            ORDER BY embedding <=> $1::vector 
            LIMIT $2
            """, 
            str(query_vector), limit
        )
        return rows
    finally:
        await conn.close()
