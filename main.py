import os #os gets environment variables
from dotenv import load_dotenv #dotenv also gets environment variables
from telebot.async_telebot import AsyncTeleBot
import asyncio
import requests # for api call
import json

# Get token from env file
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

# # Call Ergast API and make a GET request 
# def fetch_race_results():
#     url = 'http://ergast.com/api/f1/current/last/results.json' # Put .json after URL to access JSON data
#     try:
#         response = requests.get(url)
#         # Check if request was successful
#         # If the request was successful then parse the JSON response to access content
#         if response.status_code == 200:
#             results = response.json()
#             return results
#         else:
#             print(f"API request failed with status code {response.status_code}")
#             return None
#     except Exception as e:
#         print(f"An error occurred while fetching race results: {str(e)}")
#         return None
    
# # Message handlers = handles commands and then sends a msg
# # They define filters which a message must pass. If the message passes the filter, the function is called and the message is passed as an arg

# # start command - ask user to click a button to get recent race results
# @bot.message_handler(commands=['start'])
# async def start_command(message):
#     await bot.send_message(
#         message.chat.id, 
#         "Hi! Welcome to F1 Updates Bot!\n" +
#         "To get the latest F1 race results, press /raceresults.")
    
# # Access the latest race data from JSON and send race results 
# # TODO: to change this to live update
# @bot.message_handler(commands=['raceresults'])
# async def send_race_results(message):
#     try:
#         results = fetch_race_results()
#         race_name = results['MRData']['RaceTable']['Races'][0]['raceName']
#         message_text = f'Formula 1 {race_name} Race Results:\n' + 'Please press /legend for the legend\n'
    
#         for result in results['MRData']['RaceTable']['Races'][0]['Results']:
#             position = result['position']
#             driver = result['Driver']['code']
#             outcome = result['positionText']
            
#             result_str = f'{position}. {driver} ({outcome})\n'
            
#             message_text += result_str
    
#         await bot.send_message(message.chat.id, message_text)
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         await bot.send_message(message.chat.id, "An error occurred while fetching race results. Sorry and please try again later.")
        
# # Function to periodically check for the end of the race and send notification 
# async def check_race_results():
#     while True:
#         results = fetch_race_results()
        
#         # Check if the race has ended 
#         if results and 'Results' in results['MRData']['RaceTable']['Races'][0]:
#             chat_id = 123456789  # Replace with the actual chat ID where you want to send the notification
#             await send_race_results_notification(chat_id, results) # define this please

#         # Sleep for a period of time before checking again (adjust as needed)
#         await asyncio.sleep(60)  # Sleep for 1 minute 
        
# # Legend command - to show what the outcome symbol means
# @bot.message_handler(commands='legend')
# async def legend_command(message):
#     await bot.send_message(
#         message.chat.id,
#         "Legend:\n" + "Number - Finishing Position\n" + "R - Retired\n" + "D - Disqualified\n" + "E - Excluded\n" + "W - Withdrawn\n")
    

# # Polling to keep the bot running
# async def main():
#     await bot.polling()

# if __name__ == '__main__':
#     asyncio.run(main())
    
# Dictionary to store user chat IDs
user_chat_ids = {}

# Function to fetch race information from the Ergast API
def fetch_race_info(endpoint):
    url = f'http://ergast.com/api/f1/{endpoint}.json'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            race_info = response.json()
            return race_info
        else:
            print(f"API request failed with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching race information: {str(e)}")
        return None

# Function to send race information as a notification
async def send_race_info_notification(chat_id, race_info, race_type):
    try:
        message_text = f"Formula 1 {race_type} Race Information:\n"
        
        # Add logic to format and extract relevant information from race_info

        await bot.send_message(chat_id, message_text)
    except Exception as e:
        print(f"An error occurred while sending race information notification: {str(e)}")

# Function to periodically check for upcoming and past races
async def check_race_info():
    while True:
        # Fetch information about the next race
        next_race_info = fetch_race_info('current/next')

        # Fetch information about the last race
        last_race_info = fetch_race_info('current/last/results')

        # Loop through stored user chat IDs and send notifications
        for user_id, chat_id in user_chat_ids.items():
            # Send notification for the upcoming race
            if next_race_info and 'RaceTable' in next_race_info['MRData']:
                await send_race_info_notification(chat_id, next_race_info, 'Upcoming')

            # Send notification for the last race results
            if last_race_info and 'RaceTable' in last_race_info['MRData'] and 'Results' in last_race_info['MRData']['RaceTable']['Races'][0]:
                await send_race_info_notification(chat_id, last_race_info, 'Latest Results')

        # Sleep for a period of time before checking again (adjust as needed)
        await asyncio.sleep(3600)  # Sleep for 1 hour

# Handler for the /start command
@bot.message_handler(commands=['start'])
async def handle_start(message):
    # Store the user's chat ID
    user_id = message.from_user.id
    user_chat_ids[user_id] = message.chat.id

    # Send a welcome message
    await bot.send_message(message.chat.id, "Welcome to the F1 Updates Bot!")

# Start the event loop to run the asynchronous functions
async def main():
    await asyncio.gather(
        bot.polling(),
        check_race_info()
    )

if __name__ == "__main__":
    asyncio.run(main())