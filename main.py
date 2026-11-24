import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

FORCE_CHANNELS = ["p20setupallfils", "p20_letest_bypas"]
STORE_CHANNEL = "p20setupallfils"

app = Client("memories_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def check_join(client, user_id):
    for ch in FORCE_CHANNELS:
        try:
            m = await client.get_chat_member(ch, user_id)
            if m.status in ["left", "kicked"]:
                return False
        except:
            return False
    return True

def join_buttons():
    btns = []
    for ch in FORCE_CHANNELS:
        btns.append([InlineKeyboardButton(f"Join {ch}", url=f"https://t.me/{ch}")])
    btns.append([InlineKeyboardButton("✅ Try Again", callback_data="check")])
    return InlineKeyboardMarkup(btns)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    # Agar file link se aaya hai
    if len(message.command) > 1 and message.command[1].startswith("file_"):
        if not await check_join(client, message.from_user.id):
            await message.reply("**Pehle dono Channel Join karo fir Try Again dabao**", reply_markup=join_buttons())
            return
        try:
            file_id = int(message.command[1].split("_")[1])
            await client.copy_message(message.chat.id, STORE_CHANNEL, file_id)
            return
        except:
            await message.reply("File nahi mili.")
            return

    if not await check_join(client, message.from_user.id):
        await message.reply("**Pehle dono Channel Join karo fir Try Again dabao**", reply_markup=join_buttons())
        return
    await message.reply("**Welcome! File bhejo, main link bana dunga.**")

@app.on_callback_query(filters.regex("check"))
async def check_cb(client, query):
    if await check_join(client, query.from_user.id):
        await query.message.edit_text("**Welcome! File bhejo, main link bana dunga.**")
    else:
        await query.answer("Abhi bhi Join nahi kiya!", show_alert=True)

@app.on_message(filters.private & (filters.document | filters.video | filters.photo | filters.audio))
async def save_file(client, message):
    if not await check_join(client, message.from_user.id):
        await message.reply("**Pehle dono Channel Join karo fir Try Again dabao**", reply_markup=join_buttons())
        return
    msg = await message.copy(chat_id=STORE_CHANNEL)
    me = await client.get_me()
    link = f"https://t.me/{me.username}?start=file_{msg.id}"
    await message.reply(f"**Tera File Link:**\n{link}")

app.run()
