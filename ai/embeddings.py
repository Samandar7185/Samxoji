import os
from typing import List

# Simple wrapper for generating embeddings. Requires GEMINI_API_KEY in env.
try:
    import google.generativeai as genai
except Exception:
    genai = None

API_KEY = os.getenv('GEMINI_API_KEY')

async def get_embedding(text: str) -> List[float]:
    """Return embedding for the given text. If google-generativeai is not available,
    returns a zero-vector placeholder.
    """
    if genai and API_KEY:
        genai.configure(api_key=API_KEY)
        # Note: adjust model and call according to google-generativeai docs
        resp = genai.encode(text)
        return resp.get('embedding', [])
    # Fallback placeholder (small vector to avoid None)
    return [0.0] * 768
