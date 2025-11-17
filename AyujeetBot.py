import requests
import time
import random

# 🔐 Paste your Telegram Bot Token here
TELEGRAM_BOT_TOKEN = '8337172364:AAGfZB3jOPL_B9Xk4AUEC05GEs0HpK3-yMk'
BASE_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/'

# 🧠 Chatbot logic
def get_bot_response(user_input):
    user_input = user_input.lower().strip()

    greetings = [
        "Hey! How are you doing today?",
        "Hi there! 😊 What's up?",
        "Hello! Hope you're having a great day!",
        "Yo! Feeling good?"
    ]

    mood_responses = [
        "I'm just a bot, but I'm feeling chatty today! How about you?",
        "Doing awesome! Thanks for asking. What’s new with you?",
        "Feeling great! Ready to talk about anything you like.",
        "I'm good! Wanna share something fun?"
    ]

    name_responses = [
        "You can call me ChatMaster, your talkative buddy!",
        "I'm Chatster, your friendly Telegram companion!",
        "They call me Chatster. I love a good chat!",
        "Chatster here! Always ready to talk."
    ]

    bye_responses = [
        "Bye for now! Catch you later 👋",
        "See ya! Take care 😊",
        "Goodbye! It was fun chatting with you!",
        "Later, alligator 🐊"
    ]

    default_followups = [
        "Hmm, interesting... tell me more!",
        "That sounds cool. What else is on your mind?",
        "I'm listening! Go ahead.",
        "You’ve got my attention. Keep going!"
    ]

    if user_input == "/start":
        return random.choice([
            "Hey there! 👋 I'm ChatMaster, your chat buddy. Let's have a fun conversation!",
            "Hi! I'm ChatMaster 🤖. Ready to chat? Just say anything!",
            "Welcome! I'm ChatMaster. Ask me anything or just say hi!",
            "Yo! I'm ChatMaster. Let's get this convo rolling!"
        ])
    elif user_input in ["hello", "hi", "hii", "hyy", "hey"]:
        return random.choice(greetings)
    elif "how are you" in user_input or "how r u" in user_input:
        return random.choice(mood_responses)
    elif "your name" in user_input or "who are you" in user_input:
        return random.choice(name_responses)
    elif user_input in ["bye", "goodbye", "see you"]:
        return random.choice(bye_responses)
    else:
        return random.choice(default_followups)

# 📩 Send message to user
def send_message(chat_id, text):
    url = BASE_URL + 'sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)

# 🔄 Poll for new messages
def run_bot():
    print("🤖 Chatster is now running on Telegram...")
    last_update_id = None

    while True:
        url = BASE_URL + 'getUpdates'
        if last_update_id:
            url += f'?offset={last_update_id + 1}'

        response = requests.get(url)
        data = response.json()

        if 'result' in data:
            for update in data['result']:
                if 'message' in update:
                    message = update['message']
                    chat_id = message['chat']['id']
                    user_text = message.get('text', '')

                    bot_reply = get_bot_response(user_text)
                    send_message(chat_id, bot_reply)

                    last_update_id = update['update_id']

        time.sleep(1)

# 🚀 Start the bot
if __name__ == '__main__':
    run_bot()
