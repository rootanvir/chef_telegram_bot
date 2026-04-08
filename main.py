import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot

API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running!')
    def log_message(self, format, *args):
        pass

def run_server():
    port = int(os.environ.get('PORT', 8080))
    HTTPServer(('0.0.0.0', port), Handler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

HELP_MESSAGE = (
    "Here's what I can do:\n\n"
    r"🚀 /start  \- Start the bot" + "\n"
    r"❓ /help   \- Show this help message" + "\n"
    r"🎂 /cake   \- Get a cake recipe" + "\n"
)

@bot.message_handler(commands=['start'])
def welcome(message):
    name = message.from_user.first_name
    text = (
        f"Welcome, *{name}*\\! 👋\n\n"
        "I am your personal chef bot\\.\n"
        "Type /help to see what I can do\\."
    )
    bot.send_message(message.chat.id, text, parse_mode='MarkdownV2')


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, HELP_MESSAGE, parse_mode='MarkdownV2')


@bot.message_handler(commands=['cake'])
def cake_recipe(message):
    text = (
        "🎂 *Classic Cake Recipe*\n\n"
        "*Ingredients:*\n"
        "🥚 4 eggs\n"
        "🍚 ½ cup sugar\n"
        "🫙 ⅓ cup oil\n"
        "🌾 1 cup flour\n"
        "🥄 1 tsp baking powder\n"
        "✨ 2 tsp vanilla extract\n"
        "🧂 1 pinch salt\n\n"
        "*Instructions:*\n"
        "1️⃣ Beat egg whites until foamy\n"
        "2️⃣ Mix in egg yolks\n"
        "3️⃣ Add sugar & oil\n"
        "4️⃣ Fold in flour, baking powder & salt \\(use spatula, not beater\\)\n"
        "5️⃣ Stir in vanilla extract\n\n"
        "🌡 *Bake:* 170°C for 30 min 🕐"
    )
    bot.send_message(message.chat.id, text, parse_mode='MarkdownV2')


@bot.message_handler(func=lambda message: True)
def reply_func(message):
    if not message.text.startswith('/'):
        bot.reply_to(
            message,
            "I only understand commands\\. Try:\n\n" + HELP_MESSAGE,
            parse_mode='MarkdownV2'
        )


if __name__ == '__main__':
    print('Bot is running...')
    try:
        bot.polling(non_stop=True)
    except Exception as e:
        print(f'Error: {e}')