import os
import sys
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
CHANNEL_USERNAME = 'rrz9z'
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

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="{{ 'ar' if lang == 'ar' else 'en' }}" dir="{{ 'rtl' if lang == 'ar' else 'ltr' }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AboDosr Swapper - Instagram Username Transfer</title>
    <link rel="icon" href="/static/nn.png">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #e0e0e0;
            min-height: 100vh;
        }
        
        .subscription-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
        }
        
        .subscription-box {
            background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 100%);
            border: 2px solid #667eea;
            border-radius: 20px;
            padding: 40px;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
            text-align: center;
        }
        
        .subscription-box h2 {
            color: #fff;
            font-size: 28px;
            margin-bottom: 20px;
        }
        
        .subscription-box p {
            color: #b0b0b0;
            font-size: 16px;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        
        .channel-btn {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 20px;
            transition: transform 0.3s;
        }
        
        .channel-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
        }
        
        .telegram-input {
            width: 100%;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid #333;
            border-radius: 10px;
            color: white;
            font-size: 16px;
            margin-bottom: 20px;
        }
        
        .telegram-input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .verify-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.3s;
        }
        
        .verify-btn:hover {
            transform: translateY(-2px);
        }
        
        .verify-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .error-msg {
            color: #ff4444;
            font-size: 14px;
            margin-top: 10px;
        }
        
        .header {
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.95) 0%, rgba(22, 33, 62, 0.95) 100%);
            backdrop-filter: blur(20px);
            padding: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .logo img {
            width: 50px;
            height: 50px;
            border-radius: 12px;
        }
        
        .logo-text h1 {
            font-size: 22px;
            color: white;
            font-weight: bold;
        }
        
        .logo-text p {
            font-size: 12px;
            color: #888;
        }
        
        .lang-switcher {
            padding: 10px 20px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            color: white;
            cursor: pointer;
            font-weight: bold;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            background: rgba(255, 255, 255, 0.05);
            padding: 5px;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        .tab {
            flex: 1;
            padding: 15px;
            background: transparent;
            border: none;
            color: #888;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .tab.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
        }
        
        .card-title {
            font-size: 20px;
            font-weight: bold;
            color: white;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        .input-group label {
            display: block;
            color: #b0b0b0;
            margin-bottom: 8px;
            font-weight: 600;
        }
        
        .input-group input {
            width: 100%;
            padding: 15px;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            color: white;
            font-size: 14px;
        }
        
        .input-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .input-group small {
            display: block;
            color: #666;
            margin-top: 5px;
            font-size: 12px;
        }
        
        .btn-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 20px;
        }
        
        .btn {
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 14px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
            color: white;
        }
        
        .btn-success {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #f44336 0%, #da190b 100%);
            color: white;
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }
        
        .stat-card {
            background: rgba(0, 0, 0, 0.3);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #888;
            font-size: 13px;
        }
        
        .logs {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 12px;
            padding: 15px;
            height: 400px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }
        
        .log-entry {
            padding: 8px;
            margin-bottom: 8px;
            border-radius: 6px;
            border-left: 3px solid transparent;
        }
        
        .log-info { color: #2196F3; border-left-color: #2196F3; background: rgba(33, 150, 243, 0.1); }
        .log-success { color: #4CAF50; border-left-color: #4CAF50; background: rgba(76, 175, 80, 0.1); }
        .log-error { color: #f44336; border-left-color: #f44336; background: rgba(244, 67, 54, 0.1); }
        
        .contact-card {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
        }
        
        .contact-links {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        
        .contact-link {
            padding: 12px 30px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 50px;
            color: white;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .contact-link:hover {
            background: rgba(102, 126, 234, 0.3);
            border-color: #667eea;
        }
        
        @media (max-width: 768px) {
            .btn-grid {
                grid-template-columns: 1fr;
            }
            .tabs {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    {% if not verified %}
    <div class="subscription-overlay" id="subscriptionOverlay">
        <div class="subscription-box">
            <h2>{{ 'اشترك في القناة' if lang == 'ar' else 'Subscribe to Channel' }}</h2>
            <p>{{ 'للوصول الى الموقع، يجب الاشتراك في قناة التليجرام' if lang == 'ar' else 'To access the site, you must subscribe to the Telegram channel' }}</p>
            
            <a href="https://t.me/rrz9z" target="_blank" class="channel-btn">
                abo dosr programming
            </a>
            
            <input type="number" id="telegramId" class="telegram-input" placeholder="{{ 'ادخل ايدي التليجرام' if lang == 'ar' else 'Enter Telegram ID' }}">
            
            <button class="verify-btn" onclick="verifySubscription()">
                {{ 'تحقق من الاشتراك' if lang == 'ar' else 'Verify Subscription' }}
            </button>
            
            <div class="error-msg" id="errorMsg"></div>
        </div>
    </div>
    {% else %}
    <div class="header">
        <div class="header-content">
            <div class="logo">
                <img src="/static/nn.png" alt="Logo" onerror="this.style.display='none'">
                <div class="logo-text">
                    <h1>AboDosr Swapper</h1>
                    <p>Professional Transfer Tool</p>
                </div>
            </div>
            <button class="lang-switcher" onclick="switchLang()">
                {{ 'EN' if lang == 'ar' else 'AR' }}
            </button>
        </div>
    </div>
    
    <div class="container">
        <div class="tabs">
            <button class="tab active" onclick="showTab('swap')">
                {{ 'النقل' if lang == 'ar' else 'Transfer' }}
            </button>
            <button class="tab" onclick="showTab('guide')">
                {{ 'الشرح' if lang == 'ar' else 'Guide' }}
            </button>
            <button class="tab" onclick="showTab('contact')">
                {{ 'التواصل' if lang == 'ar' else 'Contact' }}
            </button>
        </div>
        
        <div id="swapTab" class="tab-content active">
            <div class="card">
                <div class="card-title">{{ 'اعدادات الحسابات' if lang == 'ar' else 'Account Settings' }}</div>
                
                <div class="input-group">
                    <label>{{ 'الحساب الرئيسي' if lang == 'ar' else 'Main Account' }}</label>
                    <input type="text" id="mainSession" placeholder="sessionid">
                    <small>{{ 'الحساب الذي سيتم النقل اليه' if lang == 'ar' else 'Account to transfer to' }}</small>
                </div>
                
                <div class="input-group">
                    <label>{{ 'الحساب المستهدف' if lang == 'ar' else 'Target Account' }}</label>
                    <input type="text" id="targetSession" placeholder="sessionid">
                    <small>{{ 'الحساب الذي يحتوي على اليوزر' if lang == 'ar' else 'Account with the username' }}</small>
                </div>
                
                <div class="input-group">
                    <label>{{ 'الحساب الاحتياطي' if lang == 'ar' else 'Backup Account' }}</label>
                    <input type="text" id="backupSession" placeholder="sessionid (optional)">
                    <small>{{ 'اختياري' if lang == 'ar' else 'Optional' }}</small>
                </div>
                
                <div class="input-group">
                    <label>{{ 'البروكسي' if lang == 'ar' else 'Proxies' }}</label>
                    <input type="text" id="proxies" placeholder="ip:port:user:pass">
                    <small>{{ 'اختياري' if lang == 'ar' else 'Optional' }}</small>
                </div>
                
                <div class="input-group">
                    <label>{{ 'الثريدات' if lang == 'ar' else 'Threads' }}</label>
                    <input type="number" id="threads" value="40" min="20" max="80">
                    <small>{{ 'يفضل 30-50' if lang == 'ar' else 'Recommended 30-50' }}</small>
                </div>
                
                <div class="btn-grid">
                    <button class="btn btn-primary" onclick="checkAccounts()">
                        {{ 'فحص' if lang == 'ar' else 'Check' }}
                    </button>
                    <button class="btn btn-success" onclick="startSwap()" id="startBtn" disabled>
                        {{ 'بدء' if lang == 'ar' else 'Start' }}
                    </button>
                    <button class="btn btn-danger" onclick="stopSwap()" id="stopBtn" disabled>
                        {{ 'ايقاف' if lang == 'ar' else 'Stop' }}
                    </button>
                </div>
            </div>
            
            <div class="card">
                <div class="card-title">{{ 'الاحصائيات' if lang == 'ar' else 'Statistics' }}</div>
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-value" id="attempts">0</div>
                        <div class="stat-label">{{ 'المحاولات' if lang == 'ar' else 'Attempts' }}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="rps">0</div>
                        <div class="stat-label">R/s</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <div class="card-title">{{ 'سجل العمليات' if lang == 'ar' else 'Operation Logs' }}</div>
                <div class="logs" id="logs">
                    <div class="log-entry log-info">{{ 'في انتظار العملية...' if lang == 'ar' else 'Waiting for operation...' }}</div>
                </div>
            </div>
        </div>
        
        <div id="guideTab" class="tab-content">
            <div class="card">
                <div class="card-title">{{ 'كيفية الاستخدام' if lang == 'ar' else 'How to Use' }}</div>
                <div style="color: #b0b0b0; line-height: 1.8;">
                    <p style="margin-bottom: 15px;">
                        {{ '1. ضع sessionid للحساب الرئيسي (الذي تريد النقل اليه)' if lang == 'ar' else '1. Enter sessionid for main account (transfer to)' }}
                    </p>
                    <p style="margin-bottom: 15px;">
                        {{ '2. ضع sessionid للحساب المستهدف (الذي يحتوي على اليوزر)' if lang == 'ar' else '2. Enter sessionid for target account (has the username)' }}
                    </p>
                    <p style="margin-bottom: 15px;">
                        {{ '3. يمكنك اضافة حساب احتياطي لزيادة فرص النجاح' if lang == 'ar' else '3. You can add backup account to increase success' }}
                    </p>
                    <p style="margin-bottom: 15px;">
                        {{ '4. اضغط فحص للتحقق من الحسابات' if lang == 'ar' else '4. Click Check to verify accounts' }}
                    </p>
                    <p>
                        {{ '5. اضغط بدء لتشغيل عملية النقل' if lang == 'ar' else '5. Click Start to begin transfer' }}
                    </p>
                </div>
            </div>
        </div>
        
        <div id="contactTab" class="tab-content">
            <div class="contact-card">
                <h2 style="color: white; margin-bottom: 10px;">{{ 'تواصل معنا' if lang == 'ar' else 'Contact Us' }}</h2>
                <p style="color: #888; margin-bottom: 20px;">{{ 'للدعم والاستفسارات' if lang == 'ar' else 'For support and inquiries' }}</p>
                
                <div class="contact-links">
                    <a href="https://t.me/AboDosr" target="_blank" class="contact-link">Telegram</a>
                    <a href="https://instagram.com/fc_c" target="_blank" class="contact-link">Instagram</a>
                    <a href="https://t.me/rrz9z" target="_blank" class="contact-link">Channel</a>
                </div>
            </div>
        </div>
    </div>
    {% endif %}
    
    <script>
        function verifySubscription() {
            const telegramId = document.getElementById('telegramId').value;
            const errorMsg = document.getElementById('errorMsg');
            
            if (!telegramId) {
                errorMsg.textContent = '{{ "ادخل الايدي" if lang == "ar" else "Enter ID" }}';
                return;
            }
            
            fetch('/verify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ telegram_id: telegramId })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    errorMsg.textContent = data.message;
                }
            });
        }
        
        function switchLang() {
            fetch('/switch_lang').then(() => location.reload());
        }
        
        function showTab(tab) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(tab + 'Tab').classList.add('active');
        }
        
        let state = {
            isRunning: false,
            attempts: 0,
            rps: 0
        };
        
        function addLog(message, type = 'info') {
            const logs = document.getElementById('logs');
            const time = new Date().toLocaleTimeString();
            logs.innerHTML += `<div class="log-entry log-${type}">[${time}] ${message}</div>`;
            logs.scrollTop = logs.scrollHeight;
        }
        
        function checkAccounts() {
            const main = document.getElementById('mainSession').value;
            const target = document.getElementById('targetSession').value;
            
            if (!main || !target) {
                addLog('{{ "ادخل السيشنات المطلوبة" if lang == "ar" else "Enter required sessions" }}', 'error');
                return;
            }
            
            addLog('{{ "جاري الفحص..." if lang == "ar" else "Checking..." }}', 'info');
            
            fetch('/check_accounts', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    main_session: main,
                    target_session: target,
                    backup_session: document.getElementById('backupSession').value
                })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    addLog(data.message, 'success');
                    document.getElementById('startBtn').disabled = false;
                } else {
                    addLog(data.message, 'error');
                }
            });
        }
        
        function startSwap() {
            state.isRunning = true;
            document.getElementById('startBtn').disabled = true;
            document.getElementById('stopBtn').disabled = false;
            
            fetch('/start_swap', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    main_session: document.getElementById('mainSession').value,
                    target_session: document.getElementById('targetSession').value,
                    backup_session: document.getElementById('backupSession').value,
                    proxies: document.getElementById('proxies').value,
                    threads: document.getElementById('threads').value
                })
            })
            .then(r => r.json())
            .then(data => {
                addLog(data.message, data.success ? 'success' : 'error');
            });
            
            updateStats();
        }
        
        function stopSwap() {
            state.isRunning = false;
            document.getElementById('startBtn').disabled = false;
            document.getElementById('stopBtn').disabled = true;
            addLog('{{ "تم الايقاف" if lang == "ar" else "Stopped" }}', 'error');
        }
        
        function updateStats() {
            if (!state.isRunning) return;
            
            fetch('/get_stats')
            .then(r => r.json())
            .then(data => {
                document.getElementById('attempts').textContent = data.attempts;
                document.getElementById('rps').textContent = data.rps;
                
                if (data.logs) {
                    data.logs.forEach(log => addLog(log.message, log.type));
                }
                
                if (state.isRunning) {
                    setTimeout(updateStats, 1000);
                }
            });
        }
    </script>
</body>
</html>
'''

# Instagram API Functions
def get_account_info(sessionid):
    try:
        response = requests.get(
            'https://www.instagram.com/api/v1/accounts/edit/web_form_data/',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'X-IG-App-ID': '936619743392459',
                'X-CSRFToken': sessionid[:32]
            },
            data={
                'first_name': account_info.get('first_name', ''),
                'email': account_info.get('email', ''),
                'username': new_username,
                'phone_number': account_info.get('phone_number', ''),
                'biography': SWAP_BIO,
                'external_url': account_info.get('external_url', ''),
                'chaining_enabled': 'on'
            },
            proxies={'http': f'http://{proxies}', 'https': f'http://{proxies}'} if proxies else None,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('status') == 'ok'
        return False
    except:
        return False

def verify_telegram_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def perform_swap(session_data):
    session = user_sessions.get(session_data['user_id'])
    if not session:
        return
    
    session.is_running = True
    target_username = session.target_info['username']
    random_username = f"{random.randint(1111, 9999)}sguu{random.randint(1111, 9999)}"
    
    try:
        if change_username(session.target_session, random_username, session.target_info):
            change_username(session.target_session, target_username, session.target_info)
            
            threads_list = []
            for _ in range(session.threads):
                if session.success:
                    break
                thread = threading.Thread(target=attempt_claim, args=(session, target_username))
                thread.start()
                threads_list.append(thread)
                time.sleep(0.1)
            
            for thread in threads_list:
                thread.join(timeout=3)
            
            if not session.success and session.backup_session:
                for _ in range(10):
                    if session.success:
                        break
                    if change_username(session.backup_session, target_username, session.backup_info):
                        session.success = True
                        send_notification(target_username, 'Backup')
                        break
                    time.sleep(0.1)
    except Exception as e:
        print(f"Swap error: {e}")
    finally:
        session.is_running = False

def attempt_claim(session, target_username):
    if session.success:
        return
    
    session.attempts += 1
    
    try:
        if change_username(session.main_session, target_username, session.main_info, session.proxies):
            session.success = True
            send_notification(target_username, 'Main')
    except:
        pass

def send_notification(username, account_type):
    try:
        hook = Webhook(WEBHOOK_URL)
        embed = Embed(
            description=f'Transfer Completed Successfully\n\nUsername: @{username}\nType: {account_type}\n\nBy insta: @fc_c & tele: @AboDosr',
            color=0x5CDBF0
        )
        embed.set_thumbnail('https://i.ibb.co/C7mtzpt/UU2-Hj-LU-Imgur-ezgif-com-video-to-gif-converter.gif')
        hook.send(embed=embed)
        
        bot.send_message(
            NOTIFICATION_CHANNEL,
            f'Transfer Completed Successfully\n\nUsername: @{username}\nType: {account_type}\n\nBy insta: @fc_c & tele: @AboDosr'
        )
    except Exception as e:
        print(f"Notification error: {e}")

# Flask Routes
@app.route('/')
def index():
    lang = session.get('lang', 'en')
    verified = session.get('verified', False)
    return render_template_string(HTML_TEMPLATE, lang=lang, verified=verified)

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
            return jsonify({'success': False, 'message': 'Not subscribed to channel'})
    except:
        return jsonify({'success': False, 'message': 'Invalid Telegram ID'})

@app.route('/switch_lang')
def switch_lang():
    current = session.get('lang', 'en')
    session['lang'] = 'ar' if current == 'en' else 'en'
    return jsonify({'success': True})

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
    swap_session.backup_session = data.get('backup_session')
    
    main_info = get_account_info(swap_session.main_session)
    target_info = get_account_info(swap_session.target_session)
    
    if not main_info or not target_info:
        return jsonify({'success': False, 'message': 'Invalid sessions'})
    
    swap_session.main_info = main_info
    swap_session.target_info = target_info
    
    if swap_session.backup_session:
        backup_info = get_account_info(swap_session.backup_session)
        if backup_info:
            swap_session.backup_info = backup_info
    
    return jsonify({
        'success': True,
        'message': f'Main: @{main_info["username"]} | Target: @{target_info["username"]}'
    })

@app.route('/start_swap', methods=['POST'])
def start_swap():
    if not session.get('verified'):
        return jsonify({'success': False, 'message': 'Not authorized'})
    
    data = request.get_json()
    user_id = session.get('telegram_id')
    
    swap_session = user_sessions.get(user_id)
    if not swap_session or not swap_session.main_info or not swap_session.target_info:
        return jsonify({'success': False, 'message': 'Please check accounts first'})
    
    swap_session.proxies = data.get('proxies')
    swap_session.threads = int(data.get('threads', 40))
    swap_session.attempts = 0
    swap_session.success = False
    
    threading.Thread(target=perform_swap, args=({'user_id': user_id},)).start()
    
    return jsonify({'success': True, 'message': 'Swap started'})

@app.route('/get_stats')
def get_stats():
    if not session.get('verified'):
        return jsonify({'attempts': 0, 'rps': 0})
    
    user_id = session.get('telegram_id')
    swap_session = user_sessions.get(user_id)
    
    if not swap_session:
        return jsonify({'attempts': 0, 'rps': 0})
    
    return jsonify({
        'attempts': swap_session.attempts,
        'rps': swap_session.attempts // 2 if swap_session.attempts > 0 else 0
    })

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)64; x64) AppleWebKit/537.36',
                'Cookie': f'sessionid={sessionid}',
                'X-IG-App-ID': '936619743392459',
                'X-CSRFToken': sessionid[:32]
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('form_data', {})
        return None
    except:
        return None

def change_username(sessionid, new_username, account_info, proxies=None):
    try:
        response = requests.post(
            'https://www.instagram.com/api/v1/web/accounts/edit/',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': f'sessionid={sessionid}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win
