import os
import requests
import json
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

API_URL = "https://echo-mind-api.vercel.app/api/kinsu?query="
user_memory = {}   # we will manage memory ourselves, not send to API


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_memory[user_id] = []
    await update.message.reply_text("Hello! I'm your AI Bot 🤖\nAsk me anything!")


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_memory[user_id] = []
    await update.message.reply_text("Memory cleared 😊")


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    msg = update.message.text

    await context.bot.send_chat_action(update.effective_chat.id, "typing")

    if user_id not in user_memory:
        user_memory[user_id] = []

    # store locally but DO NOT send to API
    user_memory[user_id].append(msg)

    try:
        # send only last message
        response = requests.get(API_URL + msg, timeout=15)
        raw_reply = response.text.strip()

        # try to parse JSON
        bot_reply = ""

        try:
            data = json.loads(raw_reply)
            bot_reply = data.get("response", "⚠️ No response field found.")
        except:
            # if API already returns plain text
            bot_reply = raw_reply

        if not bot_reply:
            bot_reply = "⚠️ API returned empty response."

    except Exception as e:
        bot_reply = "⚠️ API error or unreachable."

    # store bot reply
    user_memory[user_id].append(bot_reply)

    # send clean answer
    await update.message.reply_text(bot_reply)


async def main():
    TOKEN = os.getenv("BOT_TOKEN")

    if not TOKEN:
        print("❌ BOT_TOKEN missing!")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🚀 Bot is running...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
