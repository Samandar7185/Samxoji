# Barqaror Python 3.11 versiyasidan foydalanamiz
FROM python:3.11-slim

# Ishchi katalogni belgilash
WORKDIR /app

# Tizim paketlarini yangilash va kerakli instrumentlarni o'rnatish
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Pip-ni yangilash
RUN pip install --no-cache-dir --upgrade pip

# Kutubxonalar ro'yxatini ko'chirib o'tkazish va o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyihaning barcha fayllarini konteynerga ko'chirish
COPY . .

# Loyihani ishga tushirish buyrug'i
CMD ["python", "main.py"]
