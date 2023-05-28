from flask import Flask, request
import requests
import json
from config import TOKEN

app = Flask(__name__)

# Global dictionary to store user filter values
user_filters = {}

@app.route('/', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    message_text = data['message']['text']
    
    if message_text == '/start':
        send_message(chat_id, 'Welcome to the Chatbot! Please provide the following filters:')
        send_message(chat_id, 'Price (Enter a value):')
    elif 'Price' in message_text:
        user_filters[chat_id] = {'Price': message_text}
        send_message(chat_id, 'Service (Enter a value):')
    elif 'Service' in message_text:
        user_filters[chat_id]['Service'] = message_text
        send_message(chat_id, 'Environment (Enter a value):')
    elif 'Environment' in message_text:
        user_filters[chat_id]['Environment'] = message_text
        send_message(chat_id, 'Quality (Enter a value):')
    elif 'Quality' in message_text:
        user_filters[chat_id]['Quality'] = message_text
        send_message(chat_id, 'Thank you for providing the filters!')
        # Process the filters here
        process_filters(chat_id)
    else:
        send_message(chat_id, 'Invalid input, please try again.')
    
    return 'OK'

def process_filters(chat_id):
    filters = user_filters.get(chat_id)
    # Process the filters as needed
    # Example: Print the filters
    send_message(chat_id, f'Filters: {filters}')

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