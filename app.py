from flask import Flask, request
import requests
from config import TOKEN
import json
import io, os, sys, types
from chatbot_functions import submitting_and_next

app = Flask(__name__)

# user_filters = {}
filter_lst = []

@app.route('/', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    count = 1
    chat_id = data['message']['chat']['id']
    message_text = data['message']['text']
    
    if message_text == '/start':
        send_message(chat_id, 'Welcome to the Chatbot! Please provide the following filters:')
        send_message(chat_id, 'Price (Enter a value):')
    elif 'Price' in message_text:
        # user_filters[chat_id] = {'Price': message_text}
        filter_lst.append(message_text[6:])
        send_message(chat_id, 'Quality (Enter a value):')
    elif 'Quality' in message_text:
        # user_filters[chat_id] = {'Price': message_text}
        filter_lst.append(message_text[8:])
        send_message(chat_id, 'Environment (Enter a value):')
    # elif 'Service' in message_text:
    #     # user_filters[chat_id]['Service'] = message_text
    #     filter_lst.append(message_text)
    #     send_message(chat_id, 'Environment (Enter a value):')
    elif 'Environment' in message_text:
        # user_filters[chat_id]['Environment'] = message_text
        filter_lst.append(message_text[12:])
        send_message(chat_id, 'Food Type (Enter a value):')
    elif 'Food Type' in message_text:
        # user_filters[chat_id]['Quality'] = message_text
        filter_lst.append(message_text[10:])
        send_message(chat_id, 'Thank you for providing the filters!')
        process_filters(chat_id)
        send_message(chat_id,f"Type 'Next' to get an alternate recommendation~")
    elif 'Next' in message_text:
        next_recomendation(chat_id, count)
    else:
        send_message(chat_id, 'Invalid input, please try again.')
    
    return 'OK'

def process_filters(chat_id):
    output_dic = submitting_and_next(filter_lst)
    if len(output_dic) != 0:
        send_message(chat_id, f"Recommended restaurant: {output_dic['Restaurant']}")
        send_message(chat_id, f"Summary: {output_dic['Summary']}")
    else:
        send_message(chat_id, "No restaurant found matching the filters.")

def next_recomendation(chat_id, count):
    output_dic = submitting_and_next(filter_lst, count)
    count += 1
    if len(output_dic) != 0:
        send_message(chat_id, f"Recommended restaurant: {output_dic['Restaurant']}")
        send_message(chat_id, f"Summary: {output_dic['Summary']}")
    else:
        send_message(chat_id, "No restaurant found matching the filters.")

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    return response.json()

if __name__ == '__main__':
    app.run()
