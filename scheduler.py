from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot
from database import get_random_word, get_test_words
from datetime import datetime, timedelta
import logging

# ─── CONFIG ───────────────────────────────────────────────────────────────────
TOKEN   = "7017753518:AAEB0v66Nk4t8N1MYY16zCDjxK9zXUymOPs"
CHAT_ID = 180279593   # ← your chat ID from /debug
# ──────────────────────────────────────────────────────────────────────────────

# enable APScheduler logging
logging.getLogger("apscheduler").setLevel(logging.DEBUG)

bot = Bot(token=TOKEN)

def send_word_daily():
    logging.info("🔔 Running send_word_daily()")
    w, t = get_random_word()
    bot.send_message(chat_id=CHAT_ID, text=f"📘 Daily word:\n{w} – {t}")

def send_weekly_test():
    logging.info("🔔 Running send_weekly_test()")
    lst = get_test_words(5)
    msg = "📝 Weekly test:\n" + "\n".join(f"{i+1}. {x}" for i, x in enumerate(lst))
    bot.send_message(chat_id=CHAT_ID, text=msg)

def setup_schedulers():
    sched = BackgroundScheduler()
    run_at = datetime.now() + timedelta(minutes=1)
    logging.info(f"⏰ Scheduling test jobs for {run_at.isoformat()}")
    sched.add_job(send_word_daily,  'date', run_date=run_at)
    sched.add_job(send_weekly_test, 'date', run_date=run_at)
    sched.start()
