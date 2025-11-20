import os
import requests
import asyncio
from fastapi import FastAPI
import uvicorn

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters


API_URL = "https://echo-mind-api.vercel.app/api/niket?query="

# ---------------- FASTAPI APP ----------------
app = FastAPI()

@app.get("/")
def home():
    return {"status": "Bot deployed successfully!"}


# --------------- TELEGRAM BOT HANDLERS ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first = update.effective_user.first_name
    msg = f"👋 Hello {first}! Welcome to the bot."
    await update.message.reply_text(msg)


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    try:
        r = requests.get(API_URL + user_msg)
        data = r.json()
        bot_reply = data.get("response", "Okay")
    except Exception:
        bot_reply = "Okay"

    await update.message.reply_text(bot_reply)


# ----------- START TELEGRAM BOT IN ASYNC LOOP -----------

async def start_bot():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise Exception("BOT_TOKEN is missing in environment variables!")

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Bot started polling...")
    await application.run_polling()


# ----- MAIN STARTUP (Runs FastAPI + Telegram Bot Together) ------

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_bot())


# ------------------ RUN UVICORN ------------------

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
