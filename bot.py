import os
import requests
from fastapi import FastAPI, Request
import uvicorn
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

API_URL = "https://echo-mind-api.vercel.app/api/kinsu?query="

# ---------- FASTAPI APP ----------
app = FastAPI()

@app.get("/")
def home():
    return {"status": "Bot is running successfully!"}

# ---------- TELEGRAM BOT ----------
BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL", "https://jokewoke-bot.onrender.com")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN missing in environment!")

telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first = update.effective_user.first_name
    await update.message.reply_text(f"👋 Hello {first}! How can I help you?")

# Chat handler
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        res = requests.get(API_URL + user_text)
        js = res.json()
        reply = js.get("response", "Okay")
    except:
        reply = "API error."

    await update.message.reply_text(reply)

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

# ---------- WEBHOOK ROUTES ----------
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}

# ---------- SET WEBHOOK ON STARTUP ----------
@app.on_event("startup")
async def set_webhook():
    if RENDER_URL:
        webhook = f"{RENDER_URL}/webhook"
        await telegram_app.bot.set_webhook(webhook)
        print("Webhook set:", webhook)
    else:
        print("❌ RENDER_EXTERNAL_URL missing")

# ---------- RUN ----------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
