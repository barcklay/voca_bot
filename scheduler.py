# scheduler.py
from dotenv import load_dotenv
import os, pathlib
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot
from database import get_random_word, get_test_words
import logging

# 1. читаем .env
load_dotenv(pathlib.Path(__file__).parent / ".env")
TOKEN   = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

# 2. настраиваем бота и логгер
bot = Bot(token=TOKEN)
logging.getLogger("apscheduler").setLevel(logging.DEBUG)

# 3. задачи
def send_word_daily():
    logging.info("🔔 send_word_daily")
    w, t = get_random_word()
    bot.send_message(chat_id=CHAT_ID,
                     text=f"📘 Daily word:\n{w} – {t}")

def send_weekly_test():
    logging.info("🔔 send_weekly_test")
    lst = get_test_words(5)
    msg = "📝 Weekly test:\n" + "\n".join(f"{i+1}. {w}" for i, w in enumerate(lst))
    bot.send_message(chat_id=CHAT_ID, text=msg)

# 4. планировщик
def setup_schedulers():
    sched = BackgroundScheduler()
    logging.info("⏰ scheduling daily word and weekly test")
    # send daily word every day at 12:28
    sched.add_job(send_word_daily, "cron", hour=12, minute=28)
    # send weekly test every Monday at 09:30
    sched.add_job(send_weekly_test, "cron", day_of_week="mon", hour=9, minute=30)
    sched.start()
