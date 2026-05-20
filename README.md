# Kino Hub - Telegram Video Bot

🎬 **Telegram botiga kino va anime qidirish va yuklab berish xizmatini taqdim etuvchi platforma.**

## ✨ Xususiyatlari

- 🔍 **AI Powered Search** - Google Gemini 1.5 Flash orqali aqlli qidiruv (imlo xatolarini to'g'irlash + semantik tushunish)
- 📹 **Video Download** - Belgilangan kanallardan videolarni avtomatik yuklab olish
- 📁 **Smart Database** - PostgreSQL + PgVector bilan semantik qidiruv
- ⚡ **Real-time Monitoring** - Kanallardagi yangi videolarni doimiy kuzatish (Telethon)
- 🤖 **Telegram Integration** - Aiogram 3.x, inline tugmalar va qulay interfeys
- 🌐 **Multilingual** - O'zbek, Rus, Ingliz tillari qo'llab-quvvatlanadi

## 🏭 Arxitektura

```
├── Bot Service (Aiogram 3.x + Gemini)
├── Scraper Service (Telethon)
├── PostgreSQL + PgVector (Neon)
├── Redis (Upstash)
└── Gemini 1.5 Flash API
```

## 🚀 O'rnatish

### Talablar
- Python 3.10+
- Docker & Docker Compose
- Telegram Bot Token
- Telegram API ID & Hash
- Neon PostgreSQL (DATABASE_URL)
- Upstash Redis (REDIS_URL)
- Google Gemini API Key

### Localda ishga tushirish

```bash
git clone https://github.com/Samandar7185/Samxoji.git
cd Samxoji
git checkout feature/kino-hub-setup

cp .env.example .env
# .env faylini to'ldiring

docker-compose up -d
```

### Render.com da deploy qilish

1. Bot service yaratish
2. Scraper service yaratish
3. GitHub Secrets da quyidagilarni sozlash:
   - `RENDER_BOT_DEPLOY_HOOK`
   - `RENDER_SCRAPER_DEPLOY_HOOK`

## 🔧 Fayllar Tuzilishi

```
Samxoji/
├── bot/
│   ├── main.py
│   └── handlers/
│       ├── start.py
│       ├── search.py
│       └── download.py
├── scraper/
│   ├── main.py
│   └── monitor.py
├── database/
│   ├── connection.py
│   └── models.py
├── ai/
│   └── service.py
├── config/
│   └── settings.py
├── .github/workflows/deploy.yml
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## 📈 Buyruqlar

- `/start` - Botni ishga tushirish
- `/search <query>` - Kino qidirish (Gemini yordamida)
- Inline tugmalar orqali sifat tanlash (480p/720p/1080p)

## 🔐 GitHub Secrets

```
BOT_TOKEN
API_ID
API_HASH
SCRAPER_PHONE
DATABASE_URL
REDIS_URL
GEMINI_API_KEY
CHANNELS_TO_MONITOR
TELEGRAM_CHAT_ID
RENDER_BOT_DEPLOY_HOOK
RENDER_SCRAPER_DEPLOY_HOOK
```

## 📄 Litsenziya

MIT License

---

**Loyiha holati:** ✅ Tayyor (2026-05-20)
