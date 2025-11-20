import os
import threading
import random
import time
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, session
from flask_cors import CORS
import requests
import telebot
from dhooks import Webhook, Embed

# Configuration
BOT_TOKEN = '8501782577:AAEreC1uj6QXKqV45XJKMNqM6x42VpcbDgY'
CHANNEL_ID = '@rrz9z'
WEBHOOK_URL = 'https://discord.com/api/webhooks/1426023490942664727/eaPsqxW0lD3P7e8sA9HJTQENo4h0wjz7Tgmwpnq9A9c5R1dxoVn7ypYXAwbJnUunV0IA'
SWAP_BIO = 'Swaping By insta : @fc_c & tele : @AboDosr'
NOTIFICATION_CHANNEL = '-1003011640128'

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

user_sessions = {}

class SwapSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.main_session = None
        self.target_session = None
        self.backup_session = None
        self.proxies = None
        self.main_info = {}
        self.target_info = {}
        self.backup_info = {}
        self.threads = 40
        self.is_running = False
        self.attempts = 0
        self.success = False

# HTML Template (مختصر للتجربة)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>AboDosr Swapper</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #0a0a0a; color: white; font-family: Arial; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { color: #667eea; }
        input { width: 100%; padding: 10px; margin: 10px 0; background: #1a1a1a; border: 1px solid #333; color: white; }
        button { padding: 15px 30px; margin: 5px; background: #667eea; color: white; border: none; cursor: pointer; }
        button:hover { background: #5568d3; }
        .log { background: #1a1a1a; padding: 15px; height: 300px; overflow-y: auto; }
    </style>
</head>
<body>
    <div class="container">
        {% if not verified %}
        <h1>Subscribe to Channel</h1>
        <p>Join: <a href="https://t.me/rrz9z" target="_blank" style="color: #667eea;">abo dosr programming</a></p>
        <input type="number" id="telegramId" placeholder="Enter your Telegram ID">
        <button onclick="verify()">Verify</button>
        <div id="msg" style="color: red; margin-top: 10px;"></div>
        {% else %}
        <h1>AboDosr Instagram Swapper</h1>
        
        <h3>Main Account</h3>
        <input type="text" id="mainSession" placeholder="sessionid">
        
        <h3>Target Account</h3>
        <input type="text" id="targetSession" placeholder="sessionid">
        
        <h3>Backup (Optional)</h3>
        <input type="text" id="backupSession" placeholder="sessionid">
        
        <h3>Threads</h3>
        <input type="number" id="threads" value="40">
        
        <div>
            <button onclick="check()">Check Accounts</button>
            <button onclick="start()" id="startBtn" disabled>Start Swap</button>
        </div>
        
        <h3>Logs</h3>
        <div class="log" id="logs">Waiting...</div>
        {% endif %}
    </div>
    
    <script>
        function verify() {
            const id = document.getElementById('telegramId').value;
            fetch('/verify', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({telegram_id: id})
            })
            .then(r => r.json())
            .then(d => {
                if (d.success) location.reload();
                else document.getElementById('msg').textContent = d.message;
            });
        }
        
        function check() {
            fetch('/check_accounts', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    main_session: document.getElementById('mainSession').value,
                    target_session: document.getElementById('targetSession').value,
                    backup_session: document.getElementById('backupSession').value
                })
            })
            .then(r => r.json())
            .then(d => {
                document.getElementById('logs').innerHTML += '<div>' + d.message + '</div>';
                if (d.success) document.getElementById('startBtn').disabled = false;
            });
        }
        
        function start() {
            fetch('/start_swap', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    main_session: document.getElementById('mainSession').value,
                    target_session: document.getElementById('targetSession').value,
                    backup_session: document.getElementById('backupSession').value,
                    threads: document.getElementById('threads').value
                })
            })
            .then(r => r.json())
            .then(d => {
                document.getElementById('logs').innerHTML += '<div>' + d.message + '</div>';
            });
        }
    </script>
</body>
</html>
'''

def get_account_info(sessionid):
    try:
        response = requests.get(
            'https://www.instagram.com/api/v1/accounts/edit/web_form_data/',
            headers={
                'Cookie': f'sessionid={sessionid}',
                'X-IG-App-ID': '936619743392459'
            },
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get('form_data', {})
        return None
    except:
        return None

def verify_telegram_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@app.route('/')
def index():
    verified = session.get('verified', False)
    return render_template_string(HTML_TEMPLATE, verified=verified)

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    telegram_id = data.get('telegram_id')
    
    try:
        telegram_id = int(telegram_id)
        if verify_telegram_subscription(telegram_id):
            session['verified'] = True
            session['telegram_id'] = telegram_id
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Not subscribed'})
    except:
        return jsonify({'success': False, 'message': 'Invalid ID'})

@app.route('/check_accounts', methods=['POST'])
def check_accounts():
    if not session.get('verified'):
        return jsonify({'success': False, 'message': 'Not authorized'})
    
    data = request.get_json()
    user_id = session.get('telegram_id')
    
    if user_id not in user_sessions:
        user_sessions[user_id] = SwapSession(user_id)
    
    swap_session = user_sessions[user_id]
    swap_session.main_session = data.get('main_session')
    swap_session.target_session = data.get('target_session')
    
    main_info = get_account_info(swap_session.main_session)
    target_info = get_account_info(swap_session.target_session)
    
    if not main_info or not target_info:
        return jsonify({'success': False, 'message': 'Invalid sessions'})
    
    swap_session.main_info = main_info
    swap_session.target_info = target_info
    
    return jsonify({
        'success': True,
        'message': f'Main: @{main_info.get("username")} | Target: @{target_info.get("username")}'
    })

@app.route('/start_swap', methods=['POST'])
def start_swap():
    return jsonify({'success': True, 'message': 'Swap started (demo)'})

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
