import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client(
    "memories_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "Hi! 👋 Main Memories Bot hu.\nMujhe apni photo / video bhejo, main save kar lunga."
    )

@app.on_message(filters.photo | filters.video | filters.document)
async def save_media(client, message):
    await message.reply_text("Mil gaya! ✅ Save kar liya.")

# Fake web server for Render Free Web Service
def run_server():
    port = int(os.environ.get("PORT", 10000))
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is Live")
        def log_message(self, *args):
            pass
    HTTPServer(("0.0.0.0", port), H).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

print("Bot Started...")
app.run()
