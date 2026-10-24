import os
import re
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

def get_info(url):
    ydl_opts = {'quiet': True, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('title','No Title'), info.get('description','')[:1000]

async def start(update, context):
    await update.message.reply_text("BOT 2 LINK SIAP!\nKirim 2 link dalam 1 pesan!")

async def handle_links(update, context):
    links = re.findall(r'https?://\S+', update.message.text)
    if len(links) < 2:
        await update.message.reply_text("Kirim 2 link sekaligus dalam 1 pesan!")
        return
    await update.message.reply_text(f"Proses {len(links)} link...")
    for link in links[:2]:
        try:
            title, desc = get_info(link)
            await update.message.reply_text(f"✅ {link}\n\nJudul: {title}\n\nCaption:\n{desc}")
        except Exception as e:
            await update.message.reply_text(f"Gagal {link}: {e}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_links))
print("BOT JALAN!")
app.run_polling()
