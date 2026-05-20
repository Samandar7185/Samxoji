import asyncio
import logging
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from scraper.channels import ChannelMonitor

logger = logging.getLogger(__name__)

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

    monitor = ChannelMonitor()
    logger.info("🔍 Scraper starting...")

    while True:
        try:
            await monitor.check_channels()
            await asyncio.sleep(300)  # 5 minutes
        except Exception as e:
            logger.exception(f"Scraper error: {e}")
            await asyncio.sleep(60)


if __name__ == '__main__':
    asyncio.run(main())
