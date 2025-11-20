import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

API_URL = "https://echo-mind-api.vercel.app/api/niket?query="

# Store memory per user
user_memory = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_memory[user_id] = []

    await update.message.reply_text(
        "Hello! I'm your AI bot 🤖\n\nAsk me anything!"
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_memory[user_id] = []

    await update.message.reply_text("Memory cleared! 😊")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    # Typing animation
    await context.bot.send_chat_action(update.effective_chat.id, "typing")

    # If new user, create memory
    if user_id not in user_memory:
        user_memory[user_id] = []

    # Add user message to memory
    user_memory[user_id].append(f"User: {user_message}")

    # Take last 5 messages for context
    memory_context = "\n".join(user_memory[user_id][-5:])
    final_query = memory_context + "\nUser: " + user_message

    # API request
    try:
        response = requests.get(API_URL + final_query)
        bot_reply = response.text.strip()
    except:
        bot_reply = "⚠️ API error. Please try again later."

    # Save bot reply
    user_memory[user_id].append(f"Bot: {bot_reply}")

    await update.message.reply_text(bot_reply)

def main():
    # ✔ Get BOT_TOKEN from environment variable ONLY
    TOKEN = os.getenv("BOT_TOKEN")

    if not TOKEN:
        print("❌ ERROR: BOT_TOKEN is missing in environment!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))

    # Chat handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🚀 Bot is running successfully using BOT_TOKEN from env...")
    app.run_polling()

if __name__ == "__main__":
    main()
