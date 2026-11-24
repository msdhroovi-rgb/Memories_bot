import os
import json
import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- 1. RENDER KO JAGAYE RAKHNE KE LIYE ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- 2. MEMORIES SAVE KARNE KE LIYE ---
DATA_FILE = "memories.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

memories = load_data()

# --- 3. BOT COMMANDS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Main hu Memories Bot ❤️\n\n"
        "Mujhe koi bhi Photo, Video, File ya Text bhej do, main use save kar lunga.\n\n"
        "Commands:\n"
        "/list - Sari memories dekhne ke liye\n"
        "/clear - Sari memories delete karne ke liye\n"
        "/help - Help ke liye"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bas mujhe kuch bhej do, main save kar lunga! /list se dekh sakte ho.")

async def save_memory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    if user_id not in memories:
        memories[user_id] = []

    text = update.message.text or update.message.caption or "Media File"
    
    # Agar photo/video hai to uska file_id save karo
    file_id = None
    file_type = "text"
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        file_type = "photo"
    elif update.message.video:
        file_id = update.message.video.file_id
        file_type = "video"
    elif update.message.document:
        file_id = update.message.document.file_id
        file_type = "document"
    elif update.message.voice:
        file_id = update.message.voice.file_id
        file_type = "voice"

    memories[user_id].append({"type": file_type, "text": text, "file_id": file_id})
    save_data(memories)
    await update.message.reply_text(f"Done! ✅ Memory save ho gayi. Total: {len(memories[user_id])}")

async def list_memories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    user_mems = memories.get(user_id, [])
    if not user_mems:
        await update.message.reply_text("Abhi koi memory nahi hai. Pehle kuch bhejo!")
        return
    
    await update.message.reply_text(f"Tumhari {len(user_mems)} memories:")
    for i, m in enumerate(user_mems, 1):
        if m["type"] == "photo":
            await update.message.reply_photo(photo=m["file_id"], caption=f"{i}. {m['text']}")
        elif m["type"] == "video":
            await update.message.reply_video(video=m["file_id"], caption=f"{i}. {m['text']}")
        elif m["type"] == "document":
            await update.message.reply_document(document=m["file_id"], caption=f"{i}. {m['text']}")
        elif m["type"] == "voice":
            await update.message.reply_voice(voice=m["file_id"], caption=f"{i}. {m['text']}")
        else:
            await update.message.reply_text(f"{i}. {m['text']}")

async def clear_memories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    memories[user_id] = []
    save_data(memories)
    await update.message.reply_text("Sari memories delete kar di! 🗑️")

# --- 4. BOT CHALANE WALA MAIN PART (YEHI FIX HAI) ---
async def main_bot():
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        print("ERROR: BOT_TOKEN nahi mila!")
        return
    
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("help", help_cmd))
    app_bot.add_handler(CommandHandler("list", list_memories))
    app_bot.add_handler(CommandHandler("clear", clear_memories))
    app_bot.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, save_memory))
    
    print("Bot Started...")
    await app_bot.run_polling()

if __name__ == "__main__":
    # Flask ko alag thread me chalao - isse event loop error nahi aayega
    threading.Thread(target=run_flask, daemon=True).start()
    # Bot ko main thread me chalao
    asyncio.run(main_bot())
