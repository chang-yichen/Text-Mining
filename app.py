from flask import Flask, request
import requests
from config import TOKEN
import json

app = Flask(__name__)

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
        process_filters(chat_id)
    else:
        send_message(chat_id, 'Invalid input, please try again.')
    
    return 'OK'

def process_filters(chat_id):
    filters = user_filters.get(chat_id)
    restaurant = rank_restaurants(filters)
    if restaurant:
        send_message(chat_id, f"Restaurant matching the filters: {restaurant}")
    else:
        send_message(chat_id, "No restaurant found matching the filters.")

def rank_restaurants(filters):
    # Implement your restaurant ranking logic using the provided filters
    # Return the restaurant that matches the filters
    # Replace the code below with your ranking logic
    price_filter = filters.get('Price')
    service_filter = filters.get('Service')
    environment_filter = filters.get('Environment')
    quality_filter = filters.get('Quality')

    # Placeholder code to demonstrate the output
    if price_filter == 'cheap' and service_filter == 'excellent':
        return 'Restaurant A'
    elif price_filter == 'moderate' and service_filter == 'good':
        return 'Restaurant B'
    elif price_filter == 'expensive' and service_filter == 'poor':
        return 'Restaurant C'
    else:
        return None

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
