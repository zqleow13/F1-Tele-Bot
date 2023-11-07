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

# Call Ergast API and make a GET request 
def fetch_race_results():
    url = 'http://ergast.com/api/f1/current/last/results.json' # Put .json after URL to access JSON data
    try:
        response = requests.get(url)
        # Check if request was successful
        # If the request was successful then parse the JSON response to access content
        if response.status_code == 200:
            results = response.json()
            return results
        else:
            print(f"API request failed with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching race results: {str(e)}")
        return None
    
# Message handlers = handles commands and then sends a msg
# They define filters which a message must pass. If the message passes the filter, the function is called and the message is passed as an arg

# start command - ask user to click a button to get recent race results
@bot.message_handler(commands=['start'])
async def start_command(message):
    await bot.send_message(
        message.chat.id, 
        "Hi! Welcome to F1 Updates Bot!\n" +
        "To get the latest F1 race results, press /raceresults.")
    
# Access the latest race data from JSON and send race results 
@bot.message_handler(commands=['raceresults'])
async def send_race_results(message):
    try:
        results = fetch_race_results()
        race_name = results['MRData']['RaceTable']['Races'][0]['raceName']
        message_text = f'Formula 1 {race_name} Race Results:\n'
        
       
    
        for result in results['MRData']['RaceTable']['Races'][0]['Results']:
            position = result['position']
            driver = result['Driver']['code']
            outcome = result['positionText']
            
            
            
            result_str = f'{position}. {driver} ({outcome})\n'
            
            message_text += result_str
    
        await bot.send_message(message.chat.id, message_text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        await bot.send_message(message.chat.id, "An error occurred while fetching race results. Sorry and please try again later.")
    

# Polling to keep the bot running
async def main():
    await bot.polling()

if __name__ == '__main__':
    asyncio.run(main())