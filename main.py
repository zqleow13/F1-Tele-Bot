# this line means that whatever variable or attribute with Final should not be reassigned (think of const in JS)
from typing import Final 
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '6910715005:AAHlsn8Yd4njlcOTurOUyKGkyYYQhw9yu4g'
BOT_USERNAME: Final = '@f1_updatess_bot'

# Commands
# Start command - What do you want to tell the user when user presses start?
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply.text('Hello')

# Help command - Guide the user to use this bot
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply.text('Please type start to begin receiving race results!')


# Custom command - Whatever command that you want to give
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply.text('Please type start to begin receiving race results!')
    

# Responses

def handle_response(text: str) -> str:
    processed: str = text.lower()
    
    
    if 'hello' in proceesed:
        return 'Hey there!'
    
    if 'how are you' in processed:
        return 'I am good!'
    
    return "Sorry, I don't understand"
    
    