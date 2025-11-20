import React, { useState, useEffect } from 'react';
import { Send, Settings, Play, UserPlus, Target, Shield, Globe, MessageSquare, Instagram, ExternalLink, Check, X, Loader } from 'lucide-react';

const AboDoSrSwapper = () => {
  const [lang, setLang] = useState('ar');
  const [isSubscribed, setIsSubscribed] = useState(false);
  const [telegramId, setTelegramId] = useState('');
  const [checkingSubscription, setCheckingSubscription] = useState(false);
  const [currentPage, setCurrentPage] = useState('verification');
  const [swapData, setSwapData] = useState({
    mainSession: '',
    targetSession: '',
    backupSession: '',
    proxies: '',
    swapBio: 'Swaping By insta : @fc_c & tele : @AboDosr'
  });
  const [swapping, setSwapping] = useState(false);
  const [swapStatus, setSwapStatus] = useState([]);
  const [attempts, setAttempts] = useState(0);

  const BOT_TOKEN = "8402188295:AAH009zFY8zvgBKpqmogPeFYzWCU8reE4jU";
  const CHANNEL_ID = "-1003011640128";
  const CHANNEL_USERNAME = "@rrz9z";
  const WEBHOOK_URL = "https://discord.com/api/webhooks/1426023490942664727/eaPsqxW0lD3P7e8sA9HJTQENo4h0wjz7Tgmwpnq9A9c5R1dxoVn7ypYXAwbJnUunV0IA";

  const translations = {
    ar: {
      title: 'AboDoSr Swapper',
      subtitle: 'أداة نقل يوزرات الانستقرام',
      subscribeMsg: 'يجب الاشتراك في القناة للمتابعة',
      channelBtn: '• ᴀʙᴏ ᴅᴏsʀ ᴘʀᴏɢʀᴀᴍᴍɪɴɢ',
      telegramIdPlaceholder: 'ضع آيدي التيليجرام الخاص بك',
      verifyBtn: 'تأكيد الاشتراك',
      notSubscribed: 'لم تشترك في القناة بعد!',
      checking: 'جاري التحقق...',
      mainSession: 'Session ID - الحساب الرئيسي',
      targetSession: 'Session ID - الحساب المستهدف',
      backupSession: 'Session ID - الحساب الاحتياطي',
      proxies: 'البروكسيات (اختياري)',
      startSwap: 'بدء عملية النقل',
      swapping: 'جاري النقل...',
      home: 'الرئيسية',
      about: 'عن الموقع',
      contact: 'التواصل',
      settings: 'الإعدادات',
      aboutText: 'موقع احترافي لنقل يوزرات الانستقرام بسرعة وأمان عالي. تم تطويره بواسطة AboDosr',
      developer: 'المطور: @AboDosr',
      instagram: 'انستقرام: @fc_c',
      telegram: 'تيليجرام: @AboDosr',
      channel: 'القناة: @rrz9z',
      swapSuccess: 'تم النقل بنجاح! ✓',
      targetChanged: 'تم تغيير اليوزر المستهدف',
      mainClaimed: 'تم الاستيلاء بنجاح - الحساب الرئيسي',
      backupClaimed: 'تم الاستيلاء بنجاح - الحساب الاحتياطي'
    },
    en: {
      title: 'AboDoSr Swapper',
      subtitle: 'Instagram Username Transfer Tool',
      subscribeMsg: 'You must subscribe to the channel to continue',
      channelBtn: '• ᴀʙᴏ ᴅᴏsʀ ᴘʀᴏɢʀᴀᴍᴍɪɴɢ',
      telegramIdPlaceholder: 'Enter your Telegram ID',
      verifyBtn: 'Verify Subscription',
      notSubscribed: 'You have not subscribed yet!',
      checking: 'Checking...',
      mainSession: 'Main Account Session ID',
      targetSession: 'Target Account Session ID',
      backupSession: 'Backup Account Session ID',
      proxies: 'Proxies (Optional)',
      startSwap: 'Start Swap',
      swapping: 'Swapping...',
      home: 'Home',
      about: 'About',
      contact: 'Contact',
      settings: 'Settings',
      aboutText: 'Professional website for transferring Instagram usernames quickly and securely. Developed by AboDosr',
      developer: 'Developer: @AboDosr',
      instagram: 'Instagram: @fc_c',
      telegram: 'Telegram: @AboDosr',
      channel: 'Channel: @rrz9z',
      swapSuccess: 'Swap successful! ✓',
      targetChanged: 'Target username changed',
      mainClaimed: 'Claimed successfully - Main',
      backupClaimed: 'Claimed successfully - Backup'
    }
  };

  const t = translations[lang];

  const checkSubscription = async () => {
    if (!telegramId.trim()) {
      alert(lang === 'ar' ? 'الرجاء إدخال آيدي التيليجرام' : 'Please enter Telegram ID');
      return;
    }

    setCheckingSubscription(true);
    
    try {
      const response = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/getChatMember?chat_id=${CHANNEL_ID}&user_id=${telegramId}`);
      const data = await response.json();
      
      if (data.ok && ['member', 'administrator', 'creator'].includes(data.result.status)) {
        setIsSubscribed(true);
        setCurrentPage('home');
      } else {
        alert(t.notSubscribed);
      }
    } catch (error) {
      alert(lang === 'ar' ? 'حدث خطأ في التحقق' : 'Verification error');
    }
    
    setCheckingSubscription(false);
  };

  const getAccountInfo = async (sessionId) => {
    try {
      const response = await fetch('https://www.instagram.com/api/v1/accounts/edit/web_form_data/', {
        headers: {
          'cookie': `sessionid=${sessionId};`
        }
      });
      const data = await response.json();
      return {
        username: data.form_data.username,
        firstName: data.form_data.first_name,
        email: data.form_data.email,
        phone: data.form_data.phone_number,
        bio: data.form_data.biography,
        externalUrl: data.form_data.external_url
      };
    } catch (error) {
      return null;
    }
  };

  const changeUsername = async (sessionId, userData, newUsername) => {
    try {
      const response = await fetch('https://www.instagram.com/api/v1/web/accounts/edit/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Cookie': `sessionid=${sessionId};`
        },
        body: new URLSearchParams({
          first_name: userData.firstName,
          email: userData.email,
          username: newUsername,
          phone_number: userData.phone,
          biography: userData.bio || swapData.swapBio,
          external_url: userData.externalUrl,
          chaining_enabled: 'on'
        })
      });
      const data = await response.json();
      return data.status === 'ok';
    } catch (error) {
      return false;
    }
  };

  const startSwap = async () => {
    if (!swapData.mainSession || !swapData.targetSession) {
      alert(lang === 'ar' ? 'الرجاء إدخال Session IDs' : 'Please enter Session IDs');
      return;
    }

    setSwapping(true);
    setSwapStatus([]);
    setAttempts(0);

    const addStatus = (msg) => {
      setSwapStatus(prev => [...prev, { msg, time: new Date().toLocaleTimeString() }]);
    };

    try {
      addStatus('🔄 ' + (lang === 'ar' ? 'بدء عملية النقل...' : 'Starting swap...'));
      
      const targetInfo = await getAccountInfo(swapData.targetSession);
      if (!targetInfo) {
        addStatus('❌ ' + (lang === 'ar' ? 'خطأ في Session ID المستهدف' : 'Invalid target Session ID'));
        setSwapping(false);
        return;
      }

      const mainInfo = await getAccountInfo(swapData.mainSession);
      if (!mainInfo) {
        addStatus('❌ ' + (lang === 'ar' ? 'خطأ في Session ID الرئيسي' : 'Invalid main Session ID'));
        setSwapping(false);
        return;
      }

      const targetUsername = targetInfo.username;
      addStatus(`🎯 ${lang === 'ar' ? 'اليوزر المستهدف' : 'Target username'}: @${targetUsername}`);

      const randomUsername = `${Math.floor(Math.random() * 9000) + 1000}sguu${Math.floor(Math.random() * 9000) + 1000}`;
      
      addStatus('🔄 ' + (lang === 'ar' ? 'تغيير اليوزر المستهدف...' : 'Changing target username...'));
      const changeTarget = await changeUsername(swapData.targetSession, targetInfo, randomUsername);
      
      if (changeTarget) {
        addStatus(`✅ ${t.targetChanged} @${targetUsername} → @${randomUsername}`);
        
        let success = false;
        for (let i = 0; i < 50; i++) {
          setAttempts(i + 1);
          const claimed = await changeUsername(swapData.mainSession, mainInfo, targetUsername);
          if (claimed) {
            addStatus(`✅ ${t.mainClaimed}: @${targetUsername}`);
            success = true;
            
            await sendToTelegram(targetUsername);
            await sendToDiscord(targetUsername);
            
            break;
          }
          await new Promise(resolve => setTimeout(resolve, 200));
        }

        if (!success && swapData.backupSession) {
          const backupInfo = await getAccountInfo(swapData.backupSession);
          if (backupInfo) {
            for (let i = 0; i < 10; i++) {
              const backupClaimed = await changeUsername(swapData.backupSession, backupInfo, targetUsername);
              if (backupClaimed) {
                addStatus(`✅ ${t.backupClaimed}: @${targetUsername}`);
                await sendToTelegram(targetUsername);
                await sendToDiscord(targetUsername);
                break;
              }
            }
          }
        }

        await changeUsername(swapData.targetSession, targetInfo, targetUsername);
      } else {
        addStatus('❌ ' + (lang === 'ar' ? 'الحساب المستهدف محظور' : 'Target account blocked'));
      }
      
      addStatus('✓ ' + (lang === 'ar' ? 'انتهت العملية' : 'Process completed'));
    } catch (error) {
      addStatus('❌ ' + (lang === 'ar' ? 'حدث خطأ' : 'An error occurred'));
    }
    
    setSwapping(false);
  };

  const sendToTelegram = async (username) => {
    const message = `✓ Transfer Completed Successfully\n\nUsername: @${username}\n\nBy insta : @fc_c & tele : @AboDosr`;
    
    try {
      await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chat_id: CHANNEL_ID,
          text: message
        })
      });
    } catch (error) {
      console.error('Telegram send error:', error);
    }
  };

  const sendToDiscord = async (username) => {
    try {
      await fetch(WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          embeds: [{
            description: `✓ Transfer Completed Successfully\n\nUsername: @${username}\n\nBy insta : @fc_c & tele : @AboDosr`,
            color: 6085872,
            thumbnail: {
              url: "https://i.ibb.co/C7mtzpt/UU2-Hj-LU-Imgur-ezgif-com-video-to-gif-converter.gif"
            }
          }]
        })
      });
    } catch (error) {
      console.error('Discord send error:', error);
    }
  };

  if (!isSubscribed) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-gray-800/50 backdrop-blur-xl rounded-2xl shadow-2xl p-8 border border-purple-500/30">
          <div className="text-center mb-6">
            <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
              <Shield className="w-10 h-10 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">{t.title}</h1>
            <p className="text-gray-300">{t.subtitle}</p>
          </div>
          
          <div className="bg-purple-900/30 rounded-xl p-6 mb-6 border border-purple-500/20">
            <p className="text-white text-center mb-4">{t.subscribeMsg}</p>
            <a 
              href={`https://t.me/${CHANNEL_USERNAME.replace('@', '')}`}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 rounded-xl font-semibold flex items-center justify-center gap-2 hover:from-blue-600 hover:to-purple-700 transition-all mb-4"
            >
              <Send className="w-5 h-5" />
              {t.channelBtn}
            </a>
          </div>

          <input
            type="text"
            placeholder={t.telegramIdPlaceholder}
            value={telegramId}
            onChange={(e) => setTelegramId(e.target.value)}
            className="w-full bg-gray-700/50 border border-gray-600 rounded-xl px-4 py-3 text-white placeholder-gray-400 mb-4 focus:outline-none focus:border-purple-500 transition-all"
          />

          <button
            onClick={checkSubscription}
            disabled={checkingSubscription}
            className="w-full bg-gradient-to-r from-green-500 to-emerald-600 text-white py-3 rounded-xl font-semibold hover:from-green-600 hover:to-emerald-700 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {checkingSubscription ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                {t.checking}
              </>
            ) : (
              <>
                <Check className="w-5 h-5" />
                {t.verifyBtn}
              </>
            )}
          </button>

          <div className="mt-4 flex justify-center gap-2">
            <button onClick={() => setLang('ar')} className={`px-4 py-2 rounded-lg ${lang === 'ar' ? 'bg-purple-600 text-white' : 'bg-gray-700 text-gray-300'}`}>العربية</button>
            <button onClick={() => setLang('en')} className={`px-4 py-2 rounded-lg ${lang === 'en' ? 'bg-purple-600 text-white' : 'bg-gray-700 text-gray-300'}`}>English</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      <nav className="bg-gray-800/50 backdrop-blur-xl border-b border-purple-500/30">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <span className="text-white font-bold text-xl">{t.title}</span>
            </div>
            <div className="flex gap-2">
              <button onClick={() => setCurrentPage('home')} className={`px-4 py-2 rounded-lg ${currentPage === 'home' ? 'bg-purple-600 text-white' : 'text-gray-300 hover:bg-gray-700'}`}>{t.home}</button>
              <button onClick={() => setCurrentPage('about')} className={`px-4 py-2 rounded-lg ${currentPage === 'about' ? 'bg-purple-600 text-white' : 'text-gray-300 hover:bg-gray-700'}`}>{t.about}</button>
              <button onClick={() => setCurrentPage('contact')} className={`px-4 py-2 rounded-lg ${currentPage === 'contact' ? 'bg-purple-600 text-white' : 'text-gray-300 hover:bg-gray-700'}`}>{t.contact}</button>
              <button onClick={() => setLang(lang === 'ar' ? 'en' : 'ar')} className="px-4 py-2 rounded-lg bg-gray-700 text-white hover:bg-gray-600">
                <Globe className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {currentPage === 'home' && (
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-gray-800/50 backdrop-blur-xl rounded-2xl p-6 border border-purple-500/30">
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
                <Settings className="w-6 h-6" />
                {t.settings}
              </h2>
              
              <div className="space-y-4">
                <div>
                  <label className="text-gray-300 mb-2 block flex items-center gap-2">
                    <UserPlus className="w-4 h-4" />
                    {t.mainSession}
                  </label>
                  <input
                    type="text"
                    value={swapData.mainSession}
                    onChange={(e) => setSwapData({...swapData, mainSession: e.target.value})}
                    className="w-full bg-gray-700/50 border border-gray-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-purple-500"
                  />
                </div>

                <div>
                  <label className="text-gray-300 mb-2 block flex items-center gap-2">
                    <Target className="w-4 h-4" />
                    {t.targetSession}
                  </label>
                  <input
                    type="text"
                    value={swapData.targetSession}
                    onChange={(e) => setSwapData({...swapData, targetSession: e.target.value})}
                    className="w-full bg-gray-700/50 border border-gray-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-purple-500"
                  />
                </div>

                <div>
                  <label className="text-gray-300 mb-2 block flex items-center gap-2">
                    <Shield className="w-4 h-4" />
                    {t.backupSession}
                  </label>
                  <input
                    type="text"
                    value={swapData.backupSession}
                    onChange={(e) => setSwapData({...swapData, backupSession: e.target.value})}
                    className="w-full bg-gray-700/50 border border-gray-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-purple-500"
                  />
                </div>

                <div>
                  <label className="text-gray-300 mb-2 block">{t.proxies}</label>
                  <input
                    type="text"
                    value={swapData.proxies}
                    onChange={(e) => setSwapData({...swapData, proxies: e.target.value})}
                    placeholder="ip:port:user:pass"
                    className="w-full bg-gray-700/50 border border-gray-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-purple-500"
                  />
                </div>

                <button
                  onClick={startSwap}
                  disabled={swapping}
                  className="w-full bg-gradient-to-r from-green-500 to-emerald-600 text-white py-4 rounded-xl font-bold text-lg hover:from-green-600 hover:to-emerald-700 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
                >
                  {swapping ? (
                    <>
                      <Loader className="w-6 h-6 animate-spin" />
                      {t.swapping}
                    </>
                  ) : (
                    <>
                      <Play className="w-6 h-6" />
                      {t.startSwap}
                    </>
                  )}
                </button>
              </div>
            </div>

            <div className="bg-gray-800/50 backdrop-blur-xl rounded-2xl p-6 border border-purple-500/30">
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
                <MessageSquare className="w-6 h-6" />
                {lang === 'ar' ? 'سجل العمليات' : 'Operation Log'}
              </h2>
              
              {attempts > 0 && (
                <div className="bg-purple-900/30 rounded-xl p-4 mb-4 border border-purple-500/20">
                  <p className="text-white text-center">
                    {lang === 'ar' ? 'المحاولات' : 'Attempts'}: <span className="font-bold text-purple-400">{attempts}</span> | 
                    {lang === 'ar' ? ' السرعة' : ' Speed'}: <span className="font-bold text-green-400">{Math.floor(attempts/2)}/s</span>
                  </p>
                </div>
              )}

              <div className="bg-gray-900/50 rounded-xl p-4 h-96 overflow-y-auto space-y-2">
                {swapStatus.length === 0 ? (
                  <p className="text-gray-400 text-center">{lang === 'ar' ? 'في انتظار العمليات...' : 'Waiting for operations...'}</p>
                ) : (
                  swapStatus.map((status, i) => (
                    <div key={i} className="bg-gray-800/50 rounded-lg p-3 border-l-4 border-purple-500">
                      <p className="text-white text-sm">{status.msg}</p>
                      <p className="text-gray-400 text-xs mt-1">{status.time}</p>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        )}

        {currentPage === 'about' && (
          <div className="bg-gray-800/50 backdrop-blur-xl rounded-2xl p-8 border border-purple-500/30 max-w-3xl mx-auto">
            <h2 className="text-3xl font-bold text-white mb-6 text-center">{t.about}</h2>
            <p className="text-gray-300 text-lg text-center mb-8">{t.aboutText}</p>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-purple-900/30 rounded-xl p-6 text-center border border-purple-500/20">
                <Target className="w-12 h-12 text-purple-400 mx-auto mb-3" />
                <p className="text-white font-semibold">{lang === 'ar' ? 'سرعة عالية' : 'High Speed'}</p>
              </div>
              <div className="bg-purple-900/30 rounded-xl p-6 text-center border border-purple-500/20">
                <Shield className="w-12 h-12 text-purple-400 mx-auto mb-3" />
                <p className="text-white font-semibold">{lang === 'ar' ? 'أمان تام' : 'Full Security'}</p>
              </div>
            </div>
          </div>
        )}

        {currentPage === 'contact' && (
          <div className="bg-gray-800/50 backdrop-blur-xl rounded-2xl p-8 border border-purple-500/30 max-w-2xl mx-auto">
            <h2 className="text-3xl font-bold text-white mb-8 text-center">{t.contact}</h2>
            <div className="space-y-4">
              <a href="https://t.me/AboDosr" target="_blank" className="flex items-center gap-4 bg-purple-900/30 rounded-xl p-4 border border-purple-500/20 hover:bg-purple-900/50 transition-all">
                <Send className="w-8 h-8 text-blue-400" />
                <div>
                  <p className="text-white font-semibold">{t.developer}</p>
                  <p className="text-gray-400 text-sm">Telegram</p>
                </div>
                <ExternalLink className="w-5 h-5 text-gray-400 ml-auto" />
              </a>
              
              <a href="https://instagram.com/fc_c" target="_blank" className="flex items-center gap-4 bg-purple-900/30 rounded-xl p-4 border border-purple-500/20 hover:bg-purple-900/50 transition-all">
                <Instagram className="w-8 h-8 text-pink-400" />
                <div>
                  <p className="text-white font-semibold">{t.instagram}</p>
                  <p className="text-gray-400 text-sm">Instagram</p>
                </div>
                <ExternalLink className="w-5 h-5 text-gray-400 ml-auto" />
              </a>
              
              <a href={`https://t.me/${CHANNEL_USERNAME.replace('@', '')}`} target="_blank" className="flex items-center gap-4 bg-purple-900/30 rounded-xl p-4 border border-purple-500/20 hover:bg-purple-900/50 transition-all">
                <Send className="w-8 h-8 text-purple-400" />
                <div>
                  <p className="text-white font-semibold">{t.channel}</p>
                  <p className="text-gray-400 text-sm">• ᴀʙᴏ ᴅᴏsʀ ᴘʀᴏɢʀᴀᴍᴍɪɴɢ</p>
                </div>
                <ExternalLink className="w-5 h-5 text-gray-400 ml-auto" />
              </a>
            </div>
          </div>
        )}
      </div>

      <footer className="bg-gray-800/50 backdrop-blur-xl border-t border-purple-500/30 mt-12 py-6">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-gray-400">© 2024 AboDoSr Swapper - By @AboDosr & @fc_c</p>
        </div>
      </footer>
    </div>
  );
};

export default AboDoSrSwapper;
