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
    from flask import Flask, request, jsonify
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI", "requests", "Flask"])
    import telebot
    import requests
    from flask import Flask, request, jsonify

# ==================== Configuration ====================
CONFIG = {
    'bot_token': 'ODQwMjE4ODI5NTpBQUgwMDl6Rlk4enZnQkt0cW1vZ1BlRllXQ1VDOHJlRTRqVQ==',
    'admin_id': 'NjIwMTcyNDEwOQ==',
    'channel_id': 'LTEwMDMwMTE2NDAxMjg=',
    'webhook': 'aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTQyNjAyMzQ5MDk0MjY2NDcyNy9lYVBzcXhXMGxEM1A3ZThhUzlISlRRRU5vNGgwd2p6N1RnbXdwbnE5QTljNVIxZHhvVm43eXBZWEF3YkpuVXVuVjBJQQ==',
    'swap_bio': 'U3dhcGluZyBCeSBpbnN0YSA6IEBmY19jICYgdGVsZSA6IEBBYm9Eb3Ny'
}

def decode_config(key):
    return base64.b64decode(CONFIG[key]).decode('utf-8')

BOT_TOKEN = decode_config('bot_token')
ADMIN_ID = int(decode_config('admin_id'))
CHANNEL_ID = decode_config('channel_id')
WEBHOOK_URL = decode_config('webhook')
SWAP_BIO = decode_config('swap_bio')

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ==================== Global Variables ====================
user_sessions = {}
swap_threads = {}
swap_stats = {}

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
            'X-CSRFToken': sessionid[:32]
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
    except:
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
            'biography': account_info.get('biography', ''),
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
    except:
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
        bot.send_message(user_id, f"بدء عملية النقل...\n\nاليوزر المستهدف: @{target_username}")
        
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
                time.sleep(0.15)
            
            # Wait for threads
            for thread in threads_list:
                thread.join(timeout=2)
            
            # Step 4: Try backup if main failed
            if not session.success and session.backup_session:
                bot.send_message(user_id, "جاري المحاولة بالحساب الاحتياطي...")
                for _ in range(10):
                    if session.success:
                        break
                    
                    if change_username(session.backup_session, target_username, session.backup_info):
                        session.success = True
                        bot.send_message(user_id, f"تم النقل بنجاح بواسطة الحساب الاحتياطي")
                        send_success_notification(user_id, target_username, 'backup')
                        break
                    time.sleep(0.15)
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
            send_success_notification(session.user_id, target_username, 'main')
    except:
        pass

def send_success_notification(user_id, username, account_type):
    try:
        # Send to Discord
        webhook_data = {
            'embeds': [{
                'title': 'نقل يوزر ناجح',
                'description': f'**اليوزر:** @{username}\n**النوع:** {account_type}\n**المستخدم:** {user_id}\n\nBy insta: @fc_c & tele: @AboDosr',
                'color': 6085360,
                'thumbnail': {
                    'url': 'https://i.ibb.co/C7mtzpt/UU2-Hj-LU-Imgur-ezgif-com-video-to-gif-converter.gif'
                },
                'timestamp': datetime.utcnow().isoformat()
            }]
        }
        requests.post(WEBHOOK_URL, json=webhook_data, timeout=5)
        
        # Send to Channel
        channel_msg = f"نقل يوزر ناجح\n\nاليوزر: @{username}\nالنوع: {account_type}\nالمستخدم: {user_id}\n\nBy insta: @fc_c & tele: @AboDosr"
        bot.send_message(CHANNEL_ID, channel_msg)
    except Exception as e:
        print(f"Notification error: {e}")

# ==================== Bot Handlers ====================
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    
    if user_id != ADMIN_ID:
        bot.reply_to(message, "عذرا، هذا البوت خاص بالمطور فقط")
        return
    
    if user_id not in user_sessions:
        user_sessions[user_id] = SwapSession(user_id)
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('الحساب الرئيسي', 'حساب التارجت')
    markup.row('حساب احتياطي', 'عدد الثريدات')
    markup.row('بدء النقل', 'الاعدادات')
    
    bot.send_message(
        message.chat.id,
        "مرحبا بك في بوت نقل اليوزرات\n\nاختر احد الخيارات:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == 'الحساب الرئيسي')
def main_account_handler(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    msg = bot.send_message(message.chat.id, "ارسل سيشن الحساب الرئيسي:")
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
        bot.send_message(message.chat.id, f"تم حفظ الحساب الرئيسي: @{info['username']}")
    else:
        bot.send_message(message.chat.id, "السيشن غير صحيح، حاول مرة اخرى")

@bot.message_handler(func=lambda m: m.text == 'حساب التارجت')
def target_account_handler(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    msg = bot.send_message(message.chat.id, "ارسل سيشن حساب التارجت:")
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
        bot.send_message(message.chat.id, f"تم حفظ حساب التارجت: @{info['username']}")
    else:
        bot.send_message(message.chat.id, "السيشن غير صحيح، حاول مرة اخرى")

@bot.message_handler(func=lambda m: m.text == 'حساب احتياطي')
def backup_account_handler(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    msg = bot.send_message(message.chat.id, "ارسل سيشن الحساب الاحتياطي (اختياري):")
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
        bot.send_message(message.chat.id, f"تم حفظ الحساب الاحتياطي: @{info['username']}")
    else:
        bot.send_message(message.chat.id, "السيشن غير صحيح، حاول مرة اخرى")

@bot.message_handler(func=lambda m: m.text == 'عدد الثريدات')
def threads_handler(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    msg = bot.send_message(message.chat.id, "ارسل عدد الثريدات (يفضل 30-50):")
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
            bot.send_message(message.chat.id, f"تم تحديد عدد الثريدات: {threads}")
        else:
            bot.send_message(message.chat.id, "يجب ان يكون العدد بين 20 و 80")
    except:
        bot.send_message(message.chat.id, "ارسل رقم صحيح")

@bot.message_handler(func=lambda m: m.text == 'بدء النقل')
def start_swap_handler(message):
    user_id = message.from_user.id
    
    if user_id != ADMIN_ID:
        return
    
    session = user_sessions.get(user_id)
    
    if not session or not session.main_session or not session.target_session:
        bot.send_message(message.chat.id, "يجب تحديد الحساب الرئيسي وحساب التارجت اولا")
        return
    
    if session.is_running:
        bot.send_message(message.chat.id, "عملية نقل جارية بالفعل")
        return
    
    threading.Thread(target=perform_swap, args=(user_id,)).start()

@bot.message_handler(func=lambda m: m.text == 'الاعدادات')
def settings_handler(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    session = user_sessions.get(message.from_user.id)
    
    if not session:
        return
    
    info = f"""الاعدادات الحالية:

الحساب الرئيسي: {'✓' if session.main_session else '✗'}
حساب التارجت: {'✓' if session.target_session else '✗'}
حساب احتياطي: {'✓' if session.backup_session else '✗'}
عدد الثريدات: {session.threads}
"""
    bot.send_message(message.chat.id, info)

# ==================== Flask Routes ====================
@app.route('/')
def index():
    return 'Instagram Swapper Bot is Running'

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

# ==================== Main ====================
def run_flask():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

def run_bot():
    print("Bot is starting...")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    time.sleep(2)
    print("Starting bot polling...")
    run_bot()
