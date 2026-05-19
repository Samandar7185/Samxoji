# Bu qator Render'ga aynan qaysi Python versiyasini 
# yuklash kerakligini aniq buyuradi (3.11-slim eng barqarori)
FROM python:3.11-slim

WORKDIR /app

# Tizim paketlarini o'rnatish
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Pip va kutubxonalarni o'rnatish
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini ko'chirish
COPY . .

# Botni ishga tushirish
CMD ["python", "main.py"]
