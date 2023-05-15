from flask import Flask
from flask import request
from flask import Response
import requests
from config import TOKEN
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler

app = Flask(__name__)


def parse_message(message):
    print("message-->", message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("chat_id-->", chat_id)
    print("txt-->", txt)
    return chat_id, txt


def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }

    r = requests.post(url, json=payload)
    return r


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()

        chat_id, txt = parse_message(msg)
        if txt == "hi":
            tel_send_message(chat_id, "Hello!!")
        else:
            tel_send_message(chat_id, 'Welcome to FoodFindersBot. Please click each of the inline-button filters and set each filter~.')
            tel_send_inlinebutton(chat_id)

        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"


# def handle_message(update, context):
#     # Get the message text
#     message_text = update.message.text
#
#     # Reply to the user
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a chatbot. How can I help you?")
#
# def send_form(chat_id, context):
#     keyboard = [[KeyboardButton('Name'), KeyboardButton('Age')], [KeyboardButton('Done')]]
#     reply_markup = ReplyKeyboardMarkup(keyboard)
#     context.bot.send_message(chat_id=chat_id, text='Please fill in the form:', reply_markup=reply_markup)
#
# def handle_message(update, context):
#     # Get the message text
#     message_text = update.message.text
#
#     # Reply to the user
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a chatbot. How can I help you?")
#     send_form(update.effective_chat.id, context)

def handle_callback(update, context):
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    # Process the user input
    if data == 'Name':
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Please enter your name:')
    elif data == 'Age':
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Please enter your age:')
    elif data == 'Done':
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Thank you for submitting the form!')


# def tel_send_inlinebutton(chat_id):
#     keyboard = [
#         [InlineKeyboardButton("Price Filter", callback_data='price')],
#         [InlineKeyboardButton("Service Filter", callback_data='service')],
#         [InlineKeyboardButton("Environment Filter", callback_data='environment')],
#         [InlineKeyboardButton("Quality Filter", callback_data='quality')],
#         [InlineKeyboardButton("Submit", callback_data='submit')]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     text = "Please select a filter:"
#     url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
#     payload = {
#         'chat_id': chat_id,
#         'text': text,
#         'reply_markup': reply_markup
#     }
#     r = requests.post(url, json=payload)
#     return r

def tel_send_inlinebutton(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': "Filters:",
        'reply_markup': {
            "inline_keyboard":  [
        [
          {
            "text": "Price Filter",
            "callback_data": "Price Filter"
          }
        ],
        [
          {
            "text": "Service Filter",
            "callback_data": "Service Filter"
          }
        ],
        [
          {
            "text": "Environment Filter",
            "callback_data": "Environment Filter"
          }
        ],
        [
          {
            "text": "Quality Filter",
            "callback_data": "Quality Filter"
          }
        ],
        [
          {
            "text": "Submit",
            "callback_data": "Submit"
          }
        ]
      ]
        }
    }
    r = requests.post(url, json=payload)
    return r


if __name__ == '__main__':
    app.run(debug=True)