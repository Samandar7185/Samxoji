# Kino Hub - Telegram Video Bot

📽️ Telegram botiga video qidirish va yuklash xizmatini taqdim etuvchi platforma.

## ✨ Xususiyatlari

- 🔍 **AI Powered Search** - Gemini 1.5 Flash orqali intelligent qidiruv
- 📥 **Video Download** - Kanallardan videolarni avtomatik yuklash
- 🗄️ **Smart Database** - PgVector bilan semantik qidiruv
- ⚡ **Real-time Monitoring** - Kanallardagi yangi videolarni doimiy kuzatish
- 🤖 **Telegram Integration** - Inline buttons va komfort user interface

## 🏗️ Arxitektura

```
┌─────────────────────────────────────────┐
│         Telegram Users                  │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴──────────┐
        │                   │
    ┌───▼────────┐    ┌─────▼────────┐
    │   Bot      │    │  Scraper     │
    │ (Render)   │    │  (Render)    │
    └───┬────────┘    └─────┬────────┘
        │                   │
        └───────────┬───────┘
                    │
        ┌───────────┼────────────┐
        │           │            │
    ┌───▼───┐  ┌───▼───┐   ┌───▼──┐
    │ Neon  │  │Redis  │   │ Gemini│
    │  DB   │  │.io    │   │API    │
    └───────┘  └───────┘   └──────┘
```

## 🚀 O'rnatish

### Talablar
- Python 3.9+
- Docker & Docker Compose
- Telegram Bot Token
- Neon.com account (PostgreSQL)
- Redis.io account
- Google Gemini API key

### O'rnatish qadamlari

1. **Repository'ni clone qiling:**
```bash
git clone https://github.com/Samandar7185/Samxoji.git
cd Samxoji
git checkout feature/kino-hub-setup
```

2. **.env faylini yarating:**
```bash
cp .env.example .env
# .env ni o'z ma'lumotlaringiz bilan to'ldiring
```

3. **Docker Compose bilan ishga tushiring:**
```bash
docker-compose up -d
```

4. **Render'da deploy qiling:**
- Bot service: https://render.com
- Scraper service: https://render.com

## 📝 Sozlamalar

### GitHub Secrets
```
API_HASH
API_ID
BOT_TOKEN
DATABASE_URL
GEMINI_API_KEY
REDIS_URL
RENDER_BOT_DEPLOY_HOOK
RENDER_SCRAPER_DEPLOY_HOOK
SCRAPER_PHONE
CHANNELS_TO_MONITOR
TELEGRAM_CHAT_ID
```

## 🔧 Fayllar Tuzilishi

```
Samxoji/
├── bot/
│   ├── __init__.py
│   ├── main.py
│   └── handlers/
│       ├── start.py
│       ├── search.py
│       └── download.py
├── scraper/
│   ├── __init__.py
│   ├── main.py
│   └── channels.py
├── database/
│   ├── __init__.py
│   ├── models.py
│   └── connection.py
├── ai/
│   ├── __init__.py
│   └── embeddings.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── .github/
│   └── workflows/
│       └── deploy.yml
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## 📖 Qo'llanma

### Bot Komandalar
- `/start` - Botni ishga tushirish
- `/search <query>` - Video qidiruv
- `/channels` - Kuzatiladigan kanallar
- `/stats` - Statistika

## 🛠️ Deployment

### Local
```bash
docker-compose up
```

### Render
1. Bot service
2. Scraper service
3. Deploy hooks

## 📧 Bog'lanish

- GitHub: [@Samandar7185](https://github.com/Samandar7185)
- Telegram: [Kino Hub Bot](https://t.me/your_bot)

## 📄 Litsenziya

MIT License
