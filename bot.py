import random
import yt_dlp
import openai
import requests

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# CONFIG
API_ID = 29074185
API_HASH = "98ccddb18a6ee56582975571277610dc"
BOT_TOKEN = "8653661384:AAF81gF8GFLKmdojVhMpQhg3ZjtQy3DJWg8"
OPENAI_API = "openai_key"

openai.api_key = OPENAI_API

app = Client("superbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# USER MODE STORE
user_mode = {}

# START MENU
@app.on_message(filters.command("start"))
async def start(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 Downloader", callback_data="down"),
         InlineKeyboardButton("🤖 AI Chat", callback_data="ai")],
        [InlineKeyboardButton("🎨 Tools", callback_data="tools"),
         InlineKeyboardButton("🎮 Fun", callback_data="fun")],
        [InlineKeyboardButton("⚙️ Utility", callback_data="util"),
         InlineKeyboardButton("💎 Modes", callback_data="mode")]
    ])
    await message.reply_text("💀 Toxic Super Bot Activated\n\nSelect Option:", reply_markup=buttons)

# CALLBACK HANDLER
@app.on_callback_query()
async def cb(client, q):
    data = q.data

    if data == "down":
        await q.message.edit_text("Send link:\n/yt /ig /fb")

    elif data == "ai":
        await q.message.edit_text("Send any message to chat 🤖")

    elif data == "tools":
        await q.message.edit_text("/style /logo /bio")

    elif data == "fun":
        await q.message.edit_text("/truth /roast")

    elif data == "util":
        await q.message.edit_text("/qr /weather /translate")

    elif data == "mode":
        btn = InlineKeyboardMarkup([
            [InlineKeyboardButton("😈 Toxic", callback_data="m_toxic"),
             InlineKeyboardButton("😊 Normal", callback_data="m_normal")],
            [InlineKeyboardButton("💋 GF Mode", callback_data="m_gf")]
        ])
        await q.message.edit_text("Select AI Mode:", reply_markup=btn)

    elif data.startswith("m_"):
        mode = data.split("_")[1]
        user_mode[q.from_user.id] = mode
        await q.answer(f"Mode set to {mode} 😎", show_alert=True)

# YOUTUBE DOWNLOADER
@app.on_message(filters.command("yt"))
async def yt(client, message):
    url = message.text.split(" ",1)[1]
    await message.reply_text("Downloading...")

    ydl_opts = {'format': 'best'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file = ydl.prepare_filename(info)

    await message.reply_video(file)

# INSTAGRAM DOWNLOADER (basic)
@app.on_message(filters.command("ig"))
async def ig(client, message):
    url = message.text.split(" ",1)[1]
    api = f"https://api.douyin.wtf/api?url={url}"
    res = requests.get(api).json()

    try:
        video = res["data"]["play"]
        await message.reply_video(video)
    except:
        await message.reply_text("Failed ❌")

# AI CHAT WITH MODES
@app.on_message(filters.text & ~filters.command(["start"]))
async def ai(client, message):
    mode = user_mode.get(message.from_user.id, "normal")

    if mode == "toxic":
        prompt = f"Reply in toxic savage style: {message.text}"
    elif mode == "gf":
        prompt = f"Reply like a romantic girlfriend: {message.text}"
    else:
        prompt = message.text

    res = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    await message.reply_text(res.choices[0].message.content)

# TOOLS
@app.on_message(filters.command("style"))
async def style(client, message):
    txt = message.text.split(" ",1)[1]
    await message.reply_text(f"✨ {txt} ✨")

@app.on_message(filters.command("logo"))
async def logo(client, message):
    name = message.text.split(" ",1)[1]
    await message.reply_text(f"🔥 {name} Official")

@app.on_message(filters.command("bio"))
async def bio(client, message):
    await message.reply_text("😈 Attitude King | No Rules | Only Power")

# FUN
@app.on_message(filters.command("truth"))
async def truth(client, message):
    q = ["Crush name?", "Biggest lie?", "Secret?"]
    await message.reply_text(random.choice(q))

@app.on_message(filters.command("roast"))
async def roast(client, message):
    r = ["Tu lagta hai buffering pe paida hua 💀"]
    await message.reply_text(random.choice(r))

# QR
@app.on_message(filters.command("qr"))
async def qr(client, message):
    txt = message.text.split(" ",1)[1]
    link = f"https://api.qrserver.com/v1/create-qr-code/?data={txt}"
    await message.reply_photo(link)

# WEATHER (basic)
@app.on_message(filters.command("weather"))
async def weather(client, message):
    city = message.text.split(" ",1)[1]
    await message.reply_text(f"🌦 Weather of {city}: API add karna padega")

# TRANSLATE
@app.on_message(filters.command("translate"))
async def trans(client, message):
    await message.reply_text("🌍 Translate feature coming soon")

app.run()
