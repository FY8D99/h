import os
import sys
import subprocess
import time
import threading
import random
import json
import base64
from datetime import datetime

try:
    import telebot
    import requests
    from flask import Flask, request, jsonify, render_template_string
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", "requests", "Flask"])
    import telebot
    import requests
    from flask import Flask, request, jsonify, render_template_string

# ==================== Configuration ====================
# استخدم التوكن الصحيح مباشرة
BOT_TOKEN = '8501782577:AAEreC1uj6QXKqV45XJKMNqM6x42VpcbDgY'  # توكن البوت الجديد
ADMIN_ID = 6201724109  # الآيدي الصحيح
CHANNEL_ID = '-1003011640128'
WEBHOOK_URL = 'https://discord.com/api/webhooks/1426023490942664727/eaPsqxW0lD3P7e8sA9HJTQENo4h0wjz7Tgmwpnq9A9c5R1dxoVn7ypYXAwbJnUunV0IA'
SWAP_BIO = 'Swaping By insta : @fc_c & tele : @AboDosr'

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ==================== Global Variables ====================
user_sessions = {}

class SwapSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.main_session = None
        self.target_session = None
        self.backup_session = None
        self.main_info = {}
        self.target_info = {}
        self.backup_info = {}
        self.threads = 40
        self.is_running = False
        self.attempts = 0
        self.success = False
        
    def reset(self):
        self.is_running = False
        self.attempts = 0
        self.success = False

# ==================== Instagram API Functions ====================
def get_account_info(sessionid):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Cookie': f'sessionid={sessionid}',
            'X-IG-App-ID': '936619743392459',
            'X-CSRFToken': sessionid[:32],
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        response = requests.get(
            'https://www.instagram.com/api/v1/accounts/edit/web_form_data/',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'form_data' in data:
                return {
                    'username': data['form_data'].get('username', ''),
                    'first_name': data['form_data'].get('first_name', ''),
                    'email': data['form_data'].get('email', ''),
                    'phone_number': data['form_data'].get('phone_number', ''),
                    'biography': data['form_data'].get('biography', ''),
                    'external_url': data['form_data'].get('external_url', '')
                }
        return None
    except Exception as e:
        print(f"Error getting account info: {e}")
        return None

def change_username(sessionid, new_username, account_info):
    try:
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'sessionid={sessionid}',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/accounts/edit/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'X-CSRFToken': sessionid[:32],
            'X-IG-App-Id': '936619743392459',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        data = {
            'first_name': account_info.get('first_name', ''),
            'email': account_info.get('email', ''),
            'username': new_username,
            'phone_number': account_info.get('phone_number', ''),
            'biography': SWAP_BIO,
            'external_url': account_info.get('external_url', ''),
            'chaining_enabled': 'on'
        }
        
        response = requests.post(
            'https://www.instagram.com/api/v1/web/accounts/edit/',
            headers=headers,
            data=data,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('status') == 'ok'
        return False
    except Exception as e:
        print(f"Error changing username: {e}")
        return False

def generate_random_username():
    return f"{random.randint(1111, 9999)}sguu{random.randint(1111, 9999)}"

# ==================== Swap Logic ====================
def perform_swap(user_id):
    session = user_sessions.get(user_id)
    if not session:
        return
    
    session.is_running = True
    session.attempts = 0
    
    target_username = session.target_info['username']
    random_username = generate_random_username()
    
    try:
        bot.send_message(user_id, f"بدء عملية النقل\n\nاليوزر المستهدف: @{target_username}")
        
        # Step 1: Change target account to random username
        if change_username(session.target_session, random_username, session.target_info):
            bot.send_message(user_id, f"تم تغيير التارجت من @{target_username} الى @{random_username}")
            time.sleep(0.5)
            
            # Step 2: Change back to original to release it
            change_username(session.target_session, target_username, session.target_info)
            bot.send_message(user_id, f"تم اطلاق اليوزر @{target_username}")
            
            # Step 3: Try to claim with main account (multi-threaded)
            threads_list = []
            for _ in range(session.threads):
                if session.success:
                    break
                    
                thread = threading.Thread(
                    target=attempt_claim,
                    args=(session, target_username)
                )
                thread.start()
                threads_list.append(thread)
                time.sleep(0.1)
            
            # Wait for threads
            for thread in threads_list:
                thread.join(timeout=3)
            
            # Step 4: Try backup if main failed
            if not session.success and session.backup_session:
                bot.send_message(user_id, "جاري المحاولة بالحساب الاحتياطي...")
                for _ in range(10):
                    if session.success:
                        break
                    
                    if change_username(session.backup_session, target_username, session.backup_info):
                        session.success = True
                        bot.send_message(user_id, f"تم النقل بنجاح بواسطة الحساب الاحتياطي")
                        send_success_notification(user_id, target_username, 'Backup')
                        break
                    time.sleep(0.1)
        else:
            bot.send_message(user_id, "فشل في تغيير التارجت - الحساب محظور او السيشن خاطئ")
            
    except Exception as e:
        bot.send_message(user_id, f"حدث خطأ: {str(e)}")
    finally:
        session.reset()

def attempt_claim(session, target_username):
    if session.success:
        return
        
    session.attempts += 1
    
    try:
        if change_username(session.main_session, target_username, session.main_info):
            session.success = True
            bot.send_message(
                session.user_id,
                f"تم النقل بنجاح\n\nاليوزر: @{target_username}\nالمحاولات: {session.attempts}"
            )
            send_success_notification(session.user_id, target_username, 'Main')
    except:
        pass

def send_success_notification(user_id, username, account_type):
    try:
        # Send to Discord
        webhook_data = {
            'embeds': [{
                'title': 'Transfer Completed Successfully',
                'description': f'**Username:** @{username}\n**Type:** {account_type}\n**User ID:** {user_id}\n\nBy insta: @fc_c & tele: @AboDosr',
                'color': 6085360,
                'thumbnail': {
                    'url': 'https://i.ibb.co/C7mtzpt/UU2-Hj-LU-Imgur-ezgif-com-video-to-gif-converter.gif'
                },
                'timestamp': datetime.utcnow().isoformat()
            }]
        }
        requests.post(WEBHOOK_URL, json=webhook_data, timeout=5)
        
        # Send to Channel
        channel_msg = f"Transfer Completed Successfully\n\nUsername: @{username}\nType: {account_type}\nUser: {user_id}\n\nBy insta: @fc_c & tele: @AboDosr"
        bot.send_message(CHANNEL_ID, channel_msg)
    except Exception as e:
        print(f"Notification error: {e}")

# ==================== Bot Handlers ====================
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    
    if user_id not in user_sessions:
        user_sessions[user_id] = SwapSession(user_id)
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Main Account', 'Target Account')
    markup.row('Backup Account', 'Threads')
    markup.row('Start Swap', 'Settings')
    
    bot.send_message(
        message.chat.id,
        f"Welcome {message.from_user.first_name}\n\nInstagram Username Swapper Bot\n\nChoose an option:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == 'Main Account')
def main_account_handler(message):
    msg = bot.send_message(message.chat.id, "Send Main Account sessionid:")
    bot.register_next_step_handler(msg, process_main_session)

def process_main_session(message):
    user_id = message.from_user.id
    session = user_sessions.get(user_id)
    
    if not session:
        return
    
    session.main_session = message.text.strip()
    info = get_account_info(session.main_session)
    
    if info:
        session.main_info = info
        bot.send_message(message.chat.id, f"Main Account saved: @{info['username']}")
    else:
        bot.send_message(message.chat.id, "Invalid sessionid, try again")

@bot.message_handler(func=lambda m: m.text == 'Target Account')
def target_account_handler(message):
    msg = bot.send_message(message.chat.id, "Send Target Account sessionid:")
    bot.register_next_step_handler(msg, process_target_session)

def process_target_session(message):
    user_id = message.from_user.id
    session = user_sessions.get(user_id)
    
    if not session:
        return
    
    session.target_session = message.text.strip()
    info = get_account_info(session.target_session)
    
    if info:
        session.target_info = info
        bot.send_message(message.chat.id, f"Target Account saved: @{info['username']}")
    else:
        bot.send_message(message.chat.id, "Invalid sessionid, try again")

@bot.message_handler(func=lambda m: m.text == 'Backup Account')
def backup_account_handler(message):
    msg = bot.send_message(message.chat.id, "Send Backup Account sessionid (optional):")
    bot.register_next_step_handler(msg, process_backup_session)

def process_backup_session(message):
    user_id = message.from_user.id
    session = user_sessions.get(user_id)
    
    if not session:
        return
    
    session.backup_session = message.text.strip()
    info = get_account_info(session.backup_session)
    
    if info:
        session.backup_info = info
        bot.send_message(message.chat.id, f"Backup Account saved: @{info['username']}")
    else:
        bot.send_message(message.chat.id, "Invalid sessionid, try again")

@bot.message_handler(func=lambda m: m.text == 'Threads')
def threads_handler(message):
    msg = bot.send_message(message.chat.id, "Send number of threads (recommended 30-50):")
    bot.register_next_step_handler(msg, process_threads)

def process_threads(message):
    user_id = message.from_user.id
    session = user_sessions.get(user_id)
    
    if not session:
        return
    
    try:
        threads = int(message.text.strip())
        if 20 <= threads <= 80:
            session.threads = threads
            bot.send_message(message.chat.id, f"Threads set to: {threads}")
        else:
            bot.send_message(message.chat.id, "Number must be between 20 and 80")
    except:
        bot.send_message(message.chat.id, "Send a valid number")

@bot.message_handler(func=lambda m: m.text == 'Start Swap')
def start_swap_handler(message):
    user_id = message.from_user.id
    session = user_sessions.get(user_id)
    
    if not session or not session.main_session or not session.target_session:
        bot.send_message(message.chat.id, "Please set Main and Target accounts first")
        return
    
    if session.is_running:
        bot.send_message(message.chat.id, "Swap operation already running")
        return
    
    threading.Thread(target=perform_swap, args=(user_id,)).start()

@bot.message_handler(func=lambda m: m.text == 'Settings')
def settings_handler(message):
    session = user_sessions.get(message.from_user.id)
    
    if not session:
        return
    
    info = f"""Current Settings:

Main Account: {'✓' if session.main_session else '✗'}
Target Account: {'✓' if session.target_session else '✗'}
Backup Account: {'✓' if session.backup_session else '✗'}
Threads: {session.threads}
"""
    bot.send_message(message.chat.id, info)

# ==================== Flask Routes ====================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Swapper Bot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .container {
            text-align: center;
            padding: 40px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            max-width: 600px;
        }
        h1 {
            font-size: 48px;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        p {
            font-size: 20px;
            margin-bottom: 30px;
            opacity: 0.9;
        }
        .status {
            display: inline-block;
            padding: 12px 30px;
            background: rgba(76, 175, 80, 0.3);
            border: 2px solid #4CAF50;
            border-radius: 50px;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 30px;
        }
        .info {
            background: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 15px;
            margin-top: 30px;
        }
        .info p {
            font-size: 14px;
            margin: 8px 0;
        }
        a {
            color: #fff;
            text-decoration: none;
            font-weight: bold;
            border-bottom: 2px solid rgba(255, 255, 255, 0.5);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram Swapper Bot</h1>
        <p>Professional Username Transfer System</p>
        <div class="status">Status: Running</div>
        <div class="info">
            <p>Bot Username: <strong>@lfh_bot</strong></p>
            <p>Version: <strong>3.0 Professional</strong></p>
            <p>Developer: <a href="https://t.me/AboDosr" target="_blank">@AboDosr</a></p>
            <p>Instagram: <a href="https://instagram.com/fc_c" target="_blank">@fc_c</a></p>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'bot': 'running',
        'timestamp': datetime.now().isoformat()
    })

# ==================== Main ====================
def run_flask():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

def run_bot():
    print("Bot is starting...")
    print(f"Bot Token: {BOT_TOKEN[:20]}...")
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Bot error: {e}")
        time.sleep(5)
        run_bot()

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    time.sleep(2)
    print("Starting bot polling...")
    run_bot()
