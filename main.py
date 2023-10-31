import os #os gets environment variables
from dotenv import load_dotenv #dotenv also gets environment variables
import telebot

# Get token from env file
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Message handlers = handles commands and then sends a msg
# They define filters which a message must pass. If the message passes the filter, the function is called and the message is passed as an arg

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

bot.infinity_polling()