import os #os gets environment variables
from dotenv import load_dotenv #dotenv also gets environment variables
from telebot.async_telebot import AsyncTeleBot
import fastf1

# Get token from env file
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

# Message handlers = handles commands and then sends a msg
# They define filters which a message must pass. If the message passes the filter, the function is called and the message is passed as an arg

# start command - ask user to click a button to get recent race results
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id, 
        "Hi! I can show you the latest F1 race results. \n" +
        "To get the latest race results, press /raceresults. \n" +
        "To get help, press /help.")
    
# fetch race results
# show race results in a message

bot.infinity_polling()