from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import youtube_dl
import os
import logging

TOKEN = '7755739692:AAEA6CEH-FX5r7KkVbkoTCavDZbJIB5RNpI'

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('مرحبًا! أرسل لي رابط فيديو من YouTube وسأحاول تحميله لك.')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            with open(filename, 'rb') as video_file:
                await update.message.reply_video(video=video_file)

            os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()

if _name_ == '_main_':
    main()