import asyncio
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from aiogram import Bot as AiogramBot
from aiogram import Dispatcher
from config.settings import settings


class _HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"ok")


def start_health_server():
    port = int(os.environ.get("PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), _HealthHandler)
    server.serve_forever()


async def main():
    # Start health server thread so Render detects an open port for Web Service deployments
    threading.Thread(target=start_health_server, daemon=True).start()

    bot = AiogramBot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    # Register handlers
    from bot.handlers import start, search, download
    dp.include_router(start.router)
    dp.include_router(search.router)
    dp.include_router(download.router)

    print("🤖 Bot starting...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        # aiogram 3.x: catch generic Exception here (TelegramError no longer exported)
        print(f"Bot runtime error: {e}")


if __name__ == '__main__':
    asyncio.run(main())
