import os
import random
import time
from telebot import TeleBot

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    raise ValueError("Missing BOT_TOKEN environment variable!")

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🎲 **Welcome to Y_RNGbot!**\n\n"
        "I'm running 24/7 as a manual background worker.\n\n"
        "📥 **Commands:**\n"
        "/roll - Get a random number from 1 to 100\n"
        "/rng [min] [max] - Custom range (e.g., `/rng 5 50`)"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['roll'])
def default_roll(message):
    num = random.randint(1, 100)
    bot.reply_to(message, f"🎲 Your random number (1-100): **{num}**", parse_mode='Markdown')

@bot.message_handler(commands=['rng'])
def custom_rng(message):
    try:
        args = message.text.split()[1:]
        if len(args) != 2:
            bot.reply_to(message, "❌ Use format: `/rng 10 50`", parse_mode='Markdown')
            return
            
        low, high = int(args[0]), int(args[1])
        if low >= high:
            bot.reply_to(message, "❌ Min must be smaller than Max!")
            return
            
        num = random.randint(low, high)
        bot.reply_to(message, f"🎲 Your random number ({low}-{high}): **{num}**", parse_mode='Markdown')
    except ValueError:
        bot.reply_to(message, "❌ Please enter valid integers.", parse_mode='Markdown')

if __name__ == '__main__':
    print("Y_RNGbot Worker is spinning up...")
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"Connection dropped: {e}. Restarting loop in 5 seconds...")
            time.sleep(5)
