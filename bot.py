import os
import requests
from fastapi import FastAPI
import uvicorn
from threading import Thread

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters


API_URL = "https://echo-mind-api.vercel.app/api/kinsu?query="

app = FastAPI()

# This will show on the Render web URL
@app.get("/")
def home():
    return {"status": "Bot is running successfully!"}


# ---------- TELEGRAM BOT -----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first = update.effective_user.first_name
    welcome = f"👋 Hello {first}! Welcome to the bot. How can I help you?"
    await update.message.reply_text(welcome)


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    try:
        response = requests.get(API_URL + user_msg)
        data = response.json()
        bot_reply = data.get("response", "Okay")
    except:
        bot_reply = "API error."

    await update.message.reply_text(bot_reply)


def run_bot():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise Exception("BOT_TOKEN missing in environment!")

    app_tg = ApplicationBuilder().token(BOT_TOKEN).build()
    app_tg.add_handler(CommandHandler("start", start))
    app_tg.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app_tg.run_polling()


def start_threads():
    Thread(target=run_bot).start()


if __name__ == "__main__":
    start_threads()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
