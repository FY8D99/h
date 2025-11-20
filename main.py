<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Swaper AboDosr</title>
    <link rel="icon" type="image/png" href="nn.png">
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            color: #ffffff;
            min-height: 100vh;
            transition: all 0.3s ease;
        }

        body.ltr {
            direction: ltr;
        }

        .loading-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(10, 10, 10, 0.98);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            flex-direction: column;
            gap: 20px;
        }

        .loading-screen.hide {
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.5s ease;
        }

        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid #2a2a3e;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .subscription-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9998;
            padding: 20px;
        }

        .subscription-modal.hide {
            display: none;
        }

        .subscription-content {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 20px;
            padding: 40px;
            max-width: 400px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
            border: 1px solid rgba(102, 126, 234, 0.2);
        }

        .subscription-content h2 {
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
            font-size: 24px;
        }

        .subscription-content p {
            margin-bottom: 30px;
            color: #aaa;
            line-height: 1.6;
        }

        .sub-btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px 40px;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }

        .sub-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }

        .navbar {
            background: rgba(26, 26, 46, 0.9);
            backdrop-filter: blur(10px);
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(102, 126, 234, 0.2);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .nav-brand {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .nav-logo {
            width: 45px;
            height: 45px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }

        .nav-title {
            font-size: 20px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .lang-btn {
            background: rgba(102, 126, 234, 0.2);
            color: #667eea;
            padding: 10px 20px;
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .lang-btn:hover {
            background: rgba(102, 126, 234, 0.3);
            transform: scale(1.05);
        }

        .tabs {
            display: flex;
            background: rgba(26, 26, 46, 0.9);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(102, 126, 234, 0.2);
            overflow-x: auto;
            scrollbar-width: none;
        }

        .tabs::-webkit-scrollbar {
            display: none;
        }

        .tab {
            flex: 1;
            padding: 18px;
            text-align: center;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            white-space: nowrap;
            min-width: 100px;
            transition: all 0.3s ease;
            font-weight: 500;
        }

        .tab:hover {
            background: rgba(102, 126, 234, 0.1);
        }

        .tab.active {
            color: #667eea;
            border-bottom-color: #667eea;
            background: rgba(102, 126, 234, 0.1);
        }

        .container {
            display: none;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .container.active {
            display: block;
        }

        .user-card {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 20px;
            border: 1px solid rgba(102, 126, 234, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .user-avatar {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }

        .user-info h3 {
            color: #fff;
            margin-bottom: 8px;
            font-size: 20px;
        }

        .user-info p {
            color: #888;
            font-size: 14px;
        }

        .section {
            background: rgba(26, 26, 46, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid rgba(102, 126, 234, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .section-title {
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 20px;
        }

        .input-group {
            margin-bottom: 20px;
        }

        .input-group label {
            display: block;
            color: #aaa;
            font-size: 14px;
            margin-bottom: 10px;
            font-weight: 500;
        }

        .input-group input,
        .input-group select {
            width: 100%;
            padding: 14px 18px;
            background: rgba(10, 10, 10, 0.6);
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 12px;
            color: #fff;
            font-size: 15px;
            transition: all 0.3s ease;
        }

        .input-group input:focus,
        .input-group select:focus {
            outline: none;
            border-color: #667eea;
            background: rgba(10, 10, 10, 0.8);
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .btn-group {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 25px;
        }

        .btn {
            padding: 16px;
            border: none;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }

        .btn-success {
            background: linear-gradient(135deg, #11998e, #38ef7d);
            color: white;
        }

        .btn-danger {
            background: linear-gradient(135deg, #eb3349, #f45c43);
            color: white;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }

        .btn:active {
            transform: scale(0.98);
        }

        .status-card {
            background: rgba(10, 10, 26, 0.8);
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            border-left: 4px solid #667eea;
            display: none;
            animation: slideIn 0.5s ease;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .status-card.active {
            display: block;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .stat-item {
            background: rgba(26, 26, 46, 0.8);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid rgba(102, 126, 234, 0.2);
            transition: all 0.3s ease;
        }

        .stat-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }

        .stat-value {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        .stat-label {
            font-size: 13px;
            color: #888;
            font-weight: 500;
        }

        .about-content {
            line-height: 1.8;
            color: #aaa;
        }

        .about-content h3 {
            color: #667eea;
            margin: 25px 0 15px;
            font-size: 18px;
        }

        .about-content ul {
            margin: 15px 0 15px 25px;
        }

        .about-content li {
            margin: 10px 0;
            position: relative;
            padding-left: 10px;
        }

        .about-content li::before {
            content: "•";
            color: #667eea;
            font-weight: bold;
            position: absolute;
            left: -15px;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
        }

        .feature-card {
            background: rgba(10, 10, 26, 0.8);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid rgba(102, 126, 234, 0.2);
            transition: all 0.3s ease;
        }

        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            border-color: rgba(102, 126, 234, 0.5);
        }

        .feature-icon {
            font-size: 45px;
            margin-bottom: 15px;
        }

        .feature-title {
            font-weight: 600;
            margin-bottom: 10px;
            font-size: 16px;
        }

        .feature-desc {
            color: #888;
            font-size: 14px;
        }

        .toast {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%) translateY(150px);
            background: rgba(26, 26, 46, 0.95);
            backdrop-filter: blur(10px);
            padding: 18px 30px;
            border-radius: 12px;
            border-left: 4px solid #667eea;
            z-index: 1000;
            transition: all 0.4s ease;
            max-width: 350px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        }

        .toast.show {
            transform: translateX(-50%) translateY(0);
        }

        .toast.success {
            border-left-color: #38ef7d;
        }

        .toast.error {
            border-left-color: #eb3349;
        }
    </style>
</head>
<body>
    <div class="loading-screen" id="loadingScreen">
        <div class="spinner"></div>
        <div data-ar="جاري التحميل..." data-en="Loading...">جاري التحميل...</div>
    </div>

    <div class="subscription-modal hide" id="subscriptionModal">
        <div class="subscription-content">
            <h2 data-ar="اشتراك اجباري" data-en="Required Subscription">اشتراك اجباري</h2>
            <p data-ar="يجب الاشتراك في القناة لاستخدام الموقع" data-en="You must subscribe to the channel to use the website">يجب الاشتراك في القناة لاستخدام الموقع</p>
            <button class="sub-btn" onclick="openChannel()" data-ar="اشترك في القناة" data-en="Subscribe to Channel">اشترك في القناة</button>
            <button class="sub-btn" onclick="checkSubscription()" data-ar="تحققت من الاشتراك" data-en="I Subscribed">تحققت من الاشتراك</button>
        </div>
    </div>

    <div class="navbar">
        <div class="nav-brand">
            <div class="nav-logo">S</div>
            <div class="nav-title">Swaper AboDosr</div>
        </div>
        <button class="lang-btn" onclick="toggleLanguage()">EN</button>
    </div>

    <div class="tabs">
        <div class="tab active" onclick="showTab('home')" data-ar="الرئيسية" data-en="Home">الرئيسية</div>
        <div class="tab" onclick="showTab('about')" data-ar="عن الموقع" data-en="About">عن الموقع</div>
        <div class="tab" onclick="showTab('guide')" data-ar="طريقة الاستخدام" data-en="Guide">طريقة الاستخدام</div>
        <div class="tab" onclick="showTab('features')" data-ar="المميزات" data-en="Features">المميزات</div>
    </div>

    <div class="container active" id="home">
        <div class="user-card" id="userCard">
            <div class="user-avatar" id="userAvatar">?</div>
            <div class="user-info">
                <h3 id="userName">User</h3>
                <p id="userId">ID: 0</p>
            </div>
        </div>

        <div class="section">
            <div class="section-title" data-ar="معلومات الحسابات" data-en="Account Information">معلومات الحسابات</div>
            <div class="input-group">
                <label data-ar="Main Sessionid" data-en="Main Sessionid">Main Sessionid</label>
                <input type="text" id="mainSession" placeholder="sessionid">
            </div>
            <div class="input-group">
                <label data-ar="Target Sessionid" data-en="Target Sessionid">Target Sessionid</label>
                <input type="text" id="targetSession" placeholder="sessionid">
            </div>
            <div class="input-group">
                <label data-ar="Backup Sessionid (اختياري)" data-en="Backup Sessionid (Optional)">Backup Sessionid (اختياري)</label>
                <input type="text" id="backupSession" placeholder="sessionid">
            </div>
            <div class="input-group">
                <label data-ar="عدد الثريدات (30-50)" data-en="Threads (30-50)">عدد الثريدات (30-50)</label>
                <input type="number" id="threads" value="40" min="20" max="80">
            </div>
        </div>

        <div class="btn-group">
            <button class="btn btn-success" onclick="runSwap()">
                <span data-ar="بدء النقل" data-en="Start Swap">بدء النقل</span>
            </button>
            <button class="btn btn-primary" onclick="checkAccounts()">
                <span data-ar="فحص الحسابات" data-en="Check Accounts">فحص الحسابات</span>
            </button>
            <button class="btn btn-danger" onclick="stopSwap()">
                <span data-ar="ايقاف" data-en="Stop">ايقاف</span>
            </button>
        </div>

        <div class="status-card" id="statusCard">
            <div class="section-title" data-ar="الحالة" data-en="Status">الحالة</div>
            <div id="statusText" data-ar="جاهز" data-en="Ready">جاهز</div>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value" id="attempts">0</div>
                    <div class="stat-label" data-ar="المحاولات" data-en="Attempts">المحاولات</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="rps">0</div>
                    <div class="stat-label">R/s</div>
                </div>
            </div>
        </div>
    </div>

    <div class="container" id="about">
        <div class="section">
            <div class="section-title" data-ar="عن الموقع" data-en="About Website">عن الموقع</div>
            <div class="about-content">
                <p data-ar="Swaper AboDosr هي أداة احترافية لنقل اليوزرات في انستقرام بسرعة وكفاءة عالية. تم تطويرها باستخدام أحدث التقنيات لضمان أفضل أداء ممكن." data-en="Swaper AboDosr is a professional tool for transferring Instagram usernames quickly and efficiently. Developed using the latest technologies to ensure the best possible performance.">Swaper AboDosr هي أداة احترافية لنقل اليوزرات في انستقرام بسرعة وكفاءة عالية. تم تطويرها باستخدام أحدث التقنيات لضمان أفضل أداء ممكن.</p>
                
                <h3 data-ar="المطور" data-en="Developer">المطور</h3>
                <p data-ar="تم تطوير الموقع بواسطة @AboDosr" data-en="Developed by @AboDosr">تم تطوير الموقع بواسطة @AboDosr</p>
                <p data-ar="تيليجرام: @AboDosr | انستقرام: @fc_c" data-en="Telegram: @AboDosr | Instagram: @fc_c">تيليجرام: @AboDosr | انستقرام: @fc_c</p>
            </div>
        </div>
    </div>

    <div class="container" id="guide">
        <div class="section">
            <div class="section-title" data-ar="طريقة الاستخدام" data-en="How to Use">طريقة الاستخدام</div>
            <div class="about-content">
                <ul>
                    <li data-ar="ادخل sessionid للحساب الرئيسي (Main)" data-en="Enter the sessionid for the main account">ادخل sessionid للحساب الرئيسي (Main)</li>
                    <li data-ar="ادخل sessionid للحساب المستهدف (Target)" data-en="Enter the sessionid for the target account">ادخل sessionid للحساب المستهدف (Target)</li>
                    <li data-ar="ادخل sessionid للحساب الاحتياطي (اختياري)" data-en="Enter the sessionid for the backup account (optional)">ادخل sessionid للحساب الاحتياطي (اختياري)</li>
                    <li data-ar="اضغط على 'فحص الحسابات' للتحقق" data-en="Click 'Check Accounts' to verify">اضغط على "فحص الحسابات" للتحقق</li>
                    <li data-ar="اضغط على 'بدء النقل' لبدء العملية" data-en="Click 'Start Swap' to begin">اضغط على "بدء النقل" لبدء العملية</li>
                </ul>

                <h3 data-ar="ملاحظات مهمة" data-en="Important Notes">ملاحظات مهمة</h3>
                <ul>
                    <li data-ar="استخدم 30-50 ثريد للأفضلية" data-en="Use 30-50 threads for best results">استخدم 30-50 ثريد للأفضلية</li>
                    <li data-ar="الحساب الاحتياطي يزيد فرص النجاح" data-en="Backup account increases success rate">الحساب الاحتياطي يزيد فرص النجاح</li>
                    <li data-ar="تأكد من صحة جميع البيانات قبل البدء" data-en="Make sure all data is correct before starting">تأكد من صحة جميع البيانات قبل البدء</li>
                </ul>
            </div>
        </div>
    </div>

    <div class="container" id="features">
        <div class="section">
            <div class="section-title" data-ar="المميزات" data-en="Features">المميزات</div>
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <div class="feature-title" data-ar="سرعة فائقة" data-en="Ultra Fast">سرعة فائقة</div>
                    <div class="feature-desc" data-ar="معالجة متعددة الثريدات" data-en="Multi-threaded processing">معالجة متعددة الثريدات</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔒</div>
                    <div class="feature-title" data-ar="آمن ومستقر" data-en="Safe & Stable">آمن ومستقر</div>
                    <div class="feature-desc" data-ar="حماية من الحظر" data-en="Block protection">حماية من الحظر</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <div class="feature-title" data-ar="احصائيات مباشرة" data-en="Live Stats">احصائيات مباشرة</div>
                    <div class="feature-desc" data-ar="متابعة لحظية" data-en="Real-time tracking">متابعة لحظية</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔄</div>
                    <div class="feature-title" data-ar="حساب احتياطي" data-en="Backup Account">حساب احتياطي</div>
                    <div class="feature-desc" data-ar="زيادة فرص النجاح" data-en="Higher success rate">زيادة فرص النجاح</div>
                </div>
            </div>
        </div>
    </div>

    <div class="toast" id="toast"></div>

    <script>
        const SWAP_BIO = 'Swaping By insta : @fc_c & tele : @AboDosr';
        const CHANNEL_USERNAME = 'rrz9z';
        const CHANNEL_ID = '-1002028973833';
        const WEBHOOK_URL = 'https://discord.com/api/webhooks/1426023490942664727/eaPsqxW0lD3P7e8sA9HJTQENo4h0wjz7Tgmwpnq9A9c5R1dxoVn7ypYXAwbJnUunV0IA';
        
        let tg = window.Telegram.WebApp;
        let currentLang = 'ar';
        let swapRunning = false;
        let attempts = 0;
        let startTime = 0;
        let swapInterval = null;
        let mainInfo = {};
        let targetInfo = {};
        let backupInfo = {};

        window.addEventListener('DOMContentLoaded', () => {
            init();
        });

        async function init() {
            try {
                tg.ready();
                tg.expand();
                
                const user = tg.initDataUnsafe.user;
                if (user) {
                    document.getElementById('userName').textContent = user.first_name + (user.last_name ? ' ' + user.last_name : '');
                    document.getElementById('userId').textContent = 'ID: ' + user.id;
                    
                    const firstLetter = user.first_name.charAt(0).toUpperCase();
                    document.getElementById('userAvatar').textContent = firstLetter;
                    
                    await checkSubscription(user.id);
                } else {
                    showToast('Failed to load user data', 'error');
                }
            } catch (error) {
                console.error('Init error:', error);
                showToast('Initialization error', 'error');
            } finally {
                setTimeout(() => {
                    document.getElementById('loadingScreen').classList.add('hide');
                }, 1000);
            }
        }

        async function checkSubscription(userId) {
            try {
                const response = await fetch(`https://api.telegram.org/bot8402188295:AAH009zFY8zvgBKpqmogPeFYzWCU8reE4jU/getChatMember?chat_id=${CHANNEL_ID}&user_id=${userId}`);
                const data = await response.json();
                
                if (data.ok && ['member', 'administrator', 'creator'].includes(data.result.status)) {
                    document.getElementById('subscriptionModal').classList.add('hide');
                    return true;
                } else {
                    document.getElementById('subscriptionModal').classList.remove('hide');
                    return false;
                }
            } catch (error) {
                console.error('Subscription check error:', error);
                document.getElementById('subscriptionModal').classList.remove('hide');
                return false;
            }
        }

        function openChannel() {
            tg.openTelegramLink(`https://t.me/${CHANNEL_USERNAME}`);
        }

        function toggleLanguage() {
            currentLang = currentLang === 'ar' ? 'en' : 'ar';
            document.body.classList.toggle('ltr', currentLang === 'en');
            document.querySelector('.lang-btn').textContent = currentLang === 'ar' ? 'EN' : 'ع';
            
            document.querySelectorAll('[data-ar]').forEach(el => {
                el.textContent = el.getAttribute('data-' + currentLang);
            });
        }

        function showTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.container').forEach(c => c.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(tabName).classList.add('active');
        }

        function showToast(message, type = 'success') {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.className = `toast ${type} show`;
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        }

        function updateStatus(text) {
            const statusCard = document.getElementById('statusCard');
            const statusText = document.getElementById('statusText');
            statusCard.classList.add('active');
            statusText.innerHTML = text;
        }

        function updateStats() {
            document.getElementById('attempts').textContent = attempts;
            const elapsed = (Date.now() - startTime) / 1000;
            const rps = elapsed > 0 ? Math.round(attempts / elapsed) : 0;
            document.getElementById('rps').textContent = rps;
        }

        async function getAccountInfo(sessionid) {
            const response = await fetch('https://www.instagram.com/api/v1/accounts/edit/web_form_data/', {
                headers: {
                    'Cookie': `sessionid=${sessionid}`,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'X-IG-App-ID': '936619743392459'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                return data.form_data;
            }
            throw new Error('Invalid session');
        }

        async function checkAccounts() {
            const user = tg.initDataUnsafe.user;
            if (!user) return;
            
            const subscribed = await checkSubscription(user.id);
            if (!subscribed) {
                showToast(currentLang === 'ar' ? 'يجب الاشتراك في القناة اولا' : 'Must subscribe first', 'error');
                return;
            }

            const mainSession = document.getElementById('mainSession').value;
            const targetSession = document.getElementById('targetSession').value;
            const backupSession = document.getElementById('backupSession').value;

            if (!mainSession || !targetSession) {
                showToast(currentLang === 'ar' ? 'ادخل Main و Target' : 'Enter Main and Target', 'error');
                return;
            }

            updateStatus(currentLang === 'ar' ? 'جاري الفحص...' : 'Checking...');

            try {
                mainInfo = await getAccountInfo(mainSession);
                showToast(`Main: @${mainInfo.username}`, 'success');

                targetInfo = await getAccountInfo(targetSession);
                showToast(`Target: @${targetInfo.username}`, 'success');

                if (backupSession) {
                    backupInfo = await getAccountInfo(backupSession);
                    showToast(`Backup: @${backupInfo.username}`, 'success');
                }

                updateStatus(`${currentLang === 'ar' ? 'تم التحقق' : 'Verified'}<br>Main: @${mainInfo.username}<br>Target: @${targetInfo.username}`);
            } catch (error) {
                showToast(currentLang === 'ar' ? 'خطأ في الجلسات' : 'Invalid sessions', 'error');
                updateStatus(currentLang === 'ar' ? 'خطأ' : 'Error');
            }
        }

        async function changeUsername(sessionid, newUsername, accountInfo) {
            const response = await fetch('https://www.instagram.com/api/v1/web/accounts/edit/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Cookie': `sessionid=${sessionid}`,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'X-IG-App-ID': '936619743392459',
                    'X-CSRFToken': sessionid.substring(0, 32)
                },
                body: new URLSearchParams({
                    'first_name': accountInfo.first_name,
                    'email': accountInfo.email,
                    'username': newUsername,
                    'phone_number': accountInfo.phone_number,
                    'biography': accountInfo.biography || '',
                    'external_url': accountInfo.external_url || '',
                    'chaining_enabled': 'on'
                })
            });

            const data = await response.json();
            return data.status === 'ok';
        }

        async function runSwap() {
            const user = tg.initDataUnsafe.user;
            if (!user) return;
            
            const subscribed = await checkSubscription(user.id);
            if (!subscribed) {
                showToast(currentLang === 'ar' ? 'يجب الاشتراك في القناة اولا' : 'Must subscribe first', 'error');
                return;
            }

            if (!mainInfo.username || !targetInfo.username) {
                showToast(currentLang === 'ar' ? 'افحص الحسابات اولا' : 'Check accounts first', 'error');
                return;
            }

            if (swapRunning) {
                showToast(currentLang === 'ar' ? 'النقل يعمل بالفعل' : 'Already running', 'error');
                return;
            }

            swapRunning = true;
            attempts = 0;
            startTime = Date.now();
            updateStatus(currentLang === 'ar' ? 'جاري النقل...' : 'Swapping...');

            const targetUsername = targetInfo.username;
            const targetSession = document.getElementById('targetSession').value;
            const mainSession = document.getElementById('mainSession').value;
            const backupSession = document.getElementById('backupSession').value;
            const threads = parseInt(document.getElementById('threads').value) || 40;

            try {
                const randomUsername = `${Math.floor(Math.random() * 9000) + 1000}swap${Math.floor(Math.random() * 9000) + 1000}`;
                const targetChanged = await changeUsername(targetSession, randomUsername, targetInfo);
                
                if (targetChanged) {
                    showToast(`Target: @${targetUsername} → @${randomUsername}`, 'success');
                    
                    swapInterval = setInterval(async () => {
                        if (!swapRunning) {
                            clearInterval(swapInterval);
                            return;
                        }

                        attempts++;
                        updateStats();

                        try {
                            const mainSwapped = await changeUsername(mainSession, targetUsername, {
                                ...mainInfo,
                                biography: SWAP_BIO
                            });

                            if (mainSwapped) {
                                swapRunning = false;
                                clearInterval(swapInterval);
                                updateStatus(`${currentLang === 'ar' ? 'تم النقل بنجاح' : 'Success!'}<br>@${targetUsername}`);
                                showToast(currentLang === 'ar' ? 'تم النقل بنجاح!' : 'Swap successful!', 'success');
                                await sendWebhook(targetUsername);
                                return;
                            }

                            if (backupSession && backupInfo.username) {
                                const backupSwapped = await changeUsername(backupSession, targetUsername, {
                                    ...backupInfo,
                                    biography: SWAP_BIO
                                });

                                if (backupSwapped) {
                                    swapRunning = false;
                                    clearInterval(swapInterval);
                                    updateStatus(`${currentLang === 'ar' ? 'تم النقل (Backup)' : 'Success (Backup)!'}<br>@${targetUsername}`);
                                    showToast(currentLang === 'ar' ? 'تم النقل بالحساب الاحتياطي!' : 'Swap successful (Backup)!', 'success');
                                    await sendWebhook(targetUsername);
                                    return;
                                }
                            }
                        } catch (error) {
                            console.error('Swap attempt error:', error);
                        }
                    }, 200);
                } else {
                    showToast(currentLang === 'ar' ? 'فشل تغيير Target' : 'Failed to change target', 'error');
                    swapRunning = false;
                }
            } catch (error) {
                console.error('Swap error:', error);
                showToast(currentLang === 'ar' ? 'حدث خطأ' : 'Error occurred', 'error');
                swapRunning = false;
            }
        }

        function stopSwap() {
            swapRunning = false;
            if (swapInterval) {
                clearInterval(swapInterval);
                swapInterval = null;
            }
            showToast(currentLang === 'ar' ? 'تم الايقاف' : 'Stopped', 'success');
        }

        async function sendWebhook(username) {
            try {
                await fetch(WEBHOOK_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        embeds: [{
                            title: 'Transfer Completed Successfully',
                            description: `Username: @${username}\n\nBy insta : @fc_c & tele : @AboDosr`,
                            color: 6085872,
                            thumbnail: {
                                url: 'https://i.ibb.co/C7mtzpt/UU2-Hj-LU-Imgur-ezgif-com-video-to-gif-converter.gif'
                            }
                        }]
                    })
                });
            } catch (error) {
                console.error('Webhook error:', error);
            }
        }
