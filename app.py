from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os
import requests

app = Flask(__name__, static_folder='.')
CORS(app)

BOT_TOKEN = "8402188295:AAH009zFY8zvgBKpqmogPeFYzWCU8reE4jU"
CHANNEL_ID = "-1003011640128"

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/check-subscription', methods=['POST'])
def check_subscription():
    data = request.json
    telegram_id = data.get('telegram_id')
    
    try:
        response = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember",
            params={
                'chat_id': CHANNEL_ID,
                'user_id': telegram_id
            }
        )
        result = response.json()
        
        if result.get('ok') and result['result']['status'] in ['member', 'administrator', 'creator']:
            return jsonify({'subscribed': True})
        else:
            return jsonify({'subscribed': False})
    except Exception as e:
        return jsonify({'subscribed': False, 'error': str(e)})

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
