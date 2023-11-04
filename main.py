import os #os gets environment variables
from dotenv import load_dotenv #dotenv also gets environment variables
from telebot.async_telebot import AsyncTeleBot
import asyncio

# Get token from env file
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

# Message handlers = handles commands and then sends a msg
# They define filters which a message must pass. If the message passes the filter, the function is called and the message is passed as an arg

# start command - ask user to click a button to get recent race results
@bot.message_handler(commands=['start'])
async def start_command(message):
    await bot.send_message(
        message.chat.id, 
        "Hi! Welcome to F1 Updates Bot!\n" +
        "To get the latest F1 race results, press /raceresults.")

    
# TODO: fetch race results from Ergast API
# To show past GP results as requested for the current 2023 season - Name & Position

# show latest race results in a message
# @bot.message_handler(commands=['results'])
# async def send_f1_results(message):
#     try:
#         # Use the `await` keyword to make an asynchronous API request
#         race = await asyncio.to_thread(fastf1.get_current_session)
#         result = await asyncio.to_thread(race.get_results)
#         result_text = "\n".join([f"{i + 1}. {driver.full_name}: {driver.points} points" for i, driver in enumerate(result)])
#         await bot.send_message(message.chat.id, f"Latest F1 Race Results:\n{result_text}")
#     except Exception as e:
#         await bot.send_message(message.chat.id, f"An error occurred while fetching F1 results: {str(e)}")



# # Polling to keep the bot running
# async def main():
#     await bot.polling()

# if __name__ == '__main__':
#     asyncio.run(main())