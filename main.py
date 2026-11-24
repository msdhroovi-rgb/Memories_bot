import os
import asyncio
from pyrogram import Client, filters, idle
from aiohttp import web

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Client(
    "memories_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "Hi! 👋 Main Memories Bot hu.\nMujhe apni photo / video bhejo, main save kar lunga."
    )

@bot.on_message(filters.photo | filters.video | filters.document)
async def save_media(client, message):
    await message.reply_text("Mil gaya! ✅ Save kar liya.")

async def handle(request):
    return web.Response(text="Bot is Live")

async def main():
    # Fake server - Render Free ke liye
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 10000)))
    await site.start()
    
    print("Bot Started...")
    await bot.start()
    await idle()
    await bot.stop()

asyncio.run(main())
