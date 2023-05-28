from flask import Flask, request, Response
import requests
from config import TOKEN
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

app = Flask(__name__)

def start_command(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = "Welcome to FoodFindersBot. Please select the filter options:"
    send_inline_keyboard(chat_id, context)

def send_inline_keyboard(chat_id, context):
    keyboard = [
        [InlineKeyboardButton("Price Filter", callback_data='price')],
        [InlineKeyboardButton("Service Filter", callback_data='service')],
        [InlineKeyboardButton("Environment Filter", callback_data='environment')],
        [InlineKeyboardButton("Quality Filter", callback_data='quality')],
        [InlineKeyboardButton("Submit", callback_data='submit')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "Please select a filter:"
    context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    # Process the user input
    if data == 'price':
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Please enter the price filter:')
    elif data == 'service':
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Please enter the service filter:')
    elif data == 'environment':
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Please enter the environment filter:')
    elif data == 'quality':
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Please enter the quality filter:')
    elif data == 'submit':
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Thank you for submitting the filters!')

    # Save the filter values entered by the user
    context.user_data[data] = query.message.text


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()

        # Create an Update object from the incoming message JSON
        update = Update.de_json(msg, bot)

        # Process the update
        dispatcher.process_update(update)

        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"


if __name__ == '__main__':
    # Create the Telegram bot updater and dispatcher
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add command and callback handlers
    start_handler = CommandHandler('start', start_command)
    callback_handler = CallbackQueryHandler(handle_callback)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(callback_handler)

    # Start the bot
    updater.start_polling()
    app.run(debug=True)

