import logging, sys, asyncio
from dotenv import load_dotenv
import os, pathlib

# ── 1. грузим .env
load_dotenv(pathlib.Path(__file__).parent / ".env")

# ── 2. читаем переменные
TOKEN   = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

print("MAIN TOKEN:", TOKEN[:15], "CHAT:", CHAT_ID)   # можно убрать позже

# ── 3. теперь только подключаем telegram и scheduler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from database import add_word, get_random_word, get_test_words
from scheduler import setup_schedulers   # ← импорт теперь после load_dotenv


logging.basicConfig(level=logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Use /add word - translation")

async def add(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text[5:]
        w, tr = [s.strip() for s in text.split(" - ", 1)]
        add_word(w, tr)
        await update.message.reply_text(f"✅ Added: {w} – {tr}")
    except:
        await update.message.reply_text("❌ Use /add word - translation")

async def word(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    w, t = get_random_word()
    await update.message.reply_text(f"📘 Word of the day:\n{w} – {t}")

async def test(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lst = get_test_words(5)
    msg = "📝 Weekly test:\n" + "\n".join(f"{i+1}. {x}" for i, x in enumerate(lst))
    await update.message.reply_text(msg)

async def debug(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your chat ID is: {update.effective_chat.id}")

def main():
    if sys.platform == "darwin":
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

    app = ApplicationBuilder().token(TOKEN).build()
    # no need to delete webhook for this test

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("word", word))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("debug", debug))

    # start the test scheduler
    setup_schedulers()

    print("Bot is running…")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
