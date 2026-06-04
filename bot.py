import os
import random
from telebot import TeleBot, types

# Fetch the token from Render's environment variables for security
TOKEN = os.environ.get('BOT_TOKEN')
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🎲 **Welcome to Y_RNGbot!**\n\n"
        "I can generate random numbers for your giveaways, games, or decisions.\n\n"
        "📥 **Commands:**\n"
        "/roll - Get a random number from 1 to 100\n"
        "/rng [min] [max] - Get a number in your custom range (e.g., `/rng 5 50`)"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['roll'])
def default_roll(message):
    num = random.randint(1, 100)
    bot.reply_to(message, f"🎲 Your random number (1-100): **{num}**", parse_mode='Markdown')

@bot.message_handler(commands=['rng'])
def custom_rng(message):
    try:
        # Split the command arguments (e.g., "/rng 10 50" -> ['10', '50'])
        args = message.text.split()[1:]
        
        if len(args) != 2:
            bot.reply_to(message, "❌ Please provide both a minimum and maximum number.\nExample: `/rng 10 50`", parse_mode='Markdown')
            return
            
        low = int(args[0])
        high = int(args[1])
        
        if low >= high:
            bot.reply_to(message, "❌ The first number must be smaller than the second number!")
            return
            
        num = random.randint(low, high)
        bot.reply_to(message, f"🎲 Your random number ({low}-{high}): **{num}**", parse_mode='Markdown')
        
    except ValueError:
        bot.reply_to(message, "❌ Please enter valid integers. Example: `/rng 1 100`", parse_mode='Markdown')

if __name__ == '__main__':
    print("Y_RNGbot is spinning up...")
    bot.infinity_polling()
