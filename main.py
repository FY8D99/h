import os
import re
import subprocess
import psutil
import telebot,requests,random,time,threading,dhooks
from dhooks import Webhook
from dhooks import Webhook, Embed
from time import sleep
from threading import Thread
from random import choice,choices
from telebot import types
tok = "8501782577:AAH18TAVeOHMvV1yPC-oI-WY0pGTb9Yyr0o"
usid = "6201724109"
bot = telebot.TeleBot(tok)
swapbio = 'Swaping By insta : @fc_c & tele : @AboDosr'
swapperhok = 'https://discord.com/api/webhooks/1426023490942664727/eaPsqxW0lD3P7e8sA9HJTQENo4h0wjz7Tgmwpnq9A9c5R1dxoVn7ypYXAwbJnUunV0IA'
swappername = ''
swap_video = None
channel_id = "-1003011640128"
bmainsis = ""
bmainname = ""
bmainext = ""
bmaineml = ""
bmainbio = ""
bmainnum = ""

def proxies():
    return {
        'http': 'http://' + swapperproxies,
        'https': 'http://' + swapperproxies
    }

AccountInfo = []

class Runner:
    def __init__(self):
        self.tool_processes = {}
    def start_tool(self, bot, message, tool_name):
        tasks = os.popen("tasklist").read()
        if tool_name not in tasks:
            try:
                tool_process = subprocess.Popen([tool_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                time.sleep(1)

                self.tool_processes[tool_name] = tool_process

                if not self.is_process_running(tool_process):
                    bot.send_message(message.chat.id, f"{tool_name} has stopped.")
                    del self.tool_processes[tool_name]
            except Exception as e:
                bot.send_message(message.chat.id, f"Error starting {tool_name}: {e}")
        else:
            bot.send_message(message.chat.id, f"{tool_name} is already running.")

    def is_process_running(self, process):
        return process.poll() is None
    def stop_or_terminate(self, bot, message, tool_name):
        k=None
        procname_without_extension = tool_name.replace('.exe', '')
        for process in psutil.process_iter():
            if process.name() == tool_name:
                process.terminate()
                k = True
                if tool_name in self.tool_processes:
                    del self.tool_processes[tool_name]
                bot.send_message(message.chat.id, f"{procname_without_extension} stopped!")
                break
        if k==None:
            bot.send_message(message.chat.id, f"{procname_without_extension} not running.")

runner = Runner()

@bot.message_handler(commands=['start','close'])
def send_welcome(message):
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  button1 = types.KeyboardButton("swap")
  button2 = types.KeyboardButton("bypass")
  button4 = types.KeyboardButton("Close bypass")
  button3 = types.KeyboardButton("settings")
  keyboard.add(button1, button2, button3,button4)
  bot.send_message(usid, "Transfer Tool v3 - Unlock Feature Developer", reply_markup=keyboard)
  print("start")

@bot.message_handler(content_types=['video'])
def handle_video(message):
  global swap_video
  swap_video = message.video.file_id
  bot.send_message(message.chat.id, "$ Video saved successfully")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
  ddiddd=message.chat.id
  if 6201724109 == ddiddd:
    if "bypass" == message.text:
      bot.send_message(message.chat.id, "$ Send Sessionid")
      bot.register_next_step_handler(
    message,
    lambda m: grabberforall(m, "bypassinfo/bypass_session.txt", "Bypass Session", True)
)

    if "Close bypass" == message.text:
      runner.stop_or_terminate(bot, message, "bypassonly.exe")
    elif "bio" in message.text:
      bot.send_message(message.chat.id, "$ Send bio")
      bot.register_next_step_handler(message, set_swapbio)
    elif "Webhook" in message.text:
      bot.send_message(message.chat.id, "$ Send Webhook")
      bot.register_next_step_handler(message, swaphook)
    elif "Swapp name" in message.text:
      bot.send_message(message.chat.id, "$ Send name")
      bot.register_next_step_handler(message, namehqoq)
    elif "Video" in message.text:
      bot.send_message(message.chat.id, "$ Send Video for swap notifications")
    elif "settings" in message.text:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("bio")
        button2 = types.KeyboardButton("Webhook")
        button3 = types.KeyboardButton("Swapp name")
        button4 = types.KeyboardButton("PROXIES")
        button5 = types.KeyboardButton("Video")
        close = types.KeyboardButton("/close")
        keyboard.add(button1,button2,button3,button4,button5,close)
        bot.send_message(usid, "$ settings", reply_markup=keyboard)
    elif "swap" in message.text:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Main Sessionid")
        button2 = types.KeyboardButton("Target Sessionid")
        button3 = types.KeyboardButton("Backup Sessionid")
        close = types.KeyboardButton("/close")
        runswap = types.KeyboardButton("Run Swap")
        runswaprx = types.KeyboardButton("Run Swap with proxie")
        tthread = types.KeyboardButton("threads")
        keyboard.add(button1,button2,button3,runswap,tthread,close,runswaprx)
        bot.send_message(usid, "$ Select button", reply_markup=keyboard)
    elif "Backup Sessionid" in message.text:
      bot.send_message(message.chat.id, "$ Send Backup Sessionid")
      bot.register_next_step_handler(message, bkinfo)
    elif "PROXIES" in message.text:
      bot.send_message(message.chat.id, "$ Send Proxies")
      bot.register_next_step_handler(message, swaperprx)
    elif "Main Sessionid" in message.text:
      bot.send_message(message.chat.id, "$ Send Main Sessionid")
      bot.register_next_step_handler(message, maininfo)
    elif "Target Sessionid" in message.text:
      bot.send_message(message.chat.id, "$ Send Target Sessionid")
      bot.register_next_step_handler(message, targetinfo)
    elif "threads" in message.text:
      bot.send_message(message.chat.id, "$ Send Thread\n$ Preferably between 30 ~ 50")
      bot.register_next_step_handler(message, tthreads)
    elif "Run Swap" in message.text:
      swap()
    elif "Run Swap with proxie" in message.text:
      chprx()

  else:
    bot.reply_to(message, ddiddd)

def set_swapbio(message):
  global swapbio
  swapbio = message.text
  bot.send_message(message.chat.id, f"$ Bio set to: {message.text}")

def send_swap_notification(username):
  notification_text = f"""✓ Transfer Completed Successfully

Username: @{username}

By insta : @fc_c & tele : @AboDosr"""

  try:
    if swap_video:
      bot.send_video(usid, swap_video, caption=notification_text)
      bot.send_video(channel_id, swap_video, caption=notification_text)
    else:
      bot.send_message(usid, notification_text)
      bot.send_message(channel_id, notification_text)
  except Exception as e:
    print(f"Error sending notification: {e}")

def swapprx():
  global atts
  atts = 1
  def fk():
    time.sleep(1)
    Nusry = random.randrange(1111,9999)
    Nusryy = random.randrange(1111,9999)
    Nusrr = f"{Nusry}sguu{Nusryy}"
    swaprequest = requests.post('https://www.instagram.com/api/v1/web/accounts/edit/',headers={'Accept':'*/*','Accept-Encoding':'gzip, deflate, br, zstd','Accept-Language':'en-US,en;q=0.9','Content-Length':'172','Content-Type':'application/x-www-form-urlencoded','Cookie':f'mid=ZoELTQALAAHrrtDs_vxxGxbymHOp; ig_did=AE9A514A-C8E1-4B4D-8B75-F05ECED43315; datr=TQuBZnjQ84czQ1Q5ob4tFEOQ; ig_nrcb=1; ps_n=1; ps_l=1; csrftoken=6okPg9LlUka8srympq3b2MkTVQv37KOz; ds_user_id=4118639383; shbid="2238\0544118639383\0541751821329:01f7788977d1eec85e933ee124dd9b3461ac34281d882bd2443d15907bfd772cb94a44b7"; shbts="1720285329\0544118639383\0541751821329:01f7a6bba876091b1f50bd34e279c91ee872c2ff9db99cc9f27745ae5dd6494cea850148"; sessionid={targetsis}; rur="CLN\0544118639383\0541751892305:01f7a3d7345f1a3005d29d604aef3b77c3f479457a0bca66f2ac3626e5c120ff0cab5a02"; wd=660x679','Origin':'https://www.instagram.com','Priority':'u=1, i','Referer':'https://www.instagram.com/accounts/edit/','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"','Sec-Ch-Ua-Full-Version-List':'"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127", "Google Chrome";v="126.0.6478.127"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Model':'""','Sec-Ch-Ua-Platform':'"Windows"','Sec-Ch-Ua-Platform-Version':'"10.0.0"','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36','X-Asbd-Id':'129477','X-Csrftoken':'6okPg9LlUka8srympq3b2MkTVQv37KOz','X-Ig-App-Id':'936619743392459','X-Ig-Www-Claim':'hmac.AR2weuPJ5Xmx7A2u7KN0U3UkNj8cLYFiJttXq_hBLcASZeSg','X-Instagram-Ajax':'1014711147','X-Requested-With':'XMLHttpRequest',},data={'first_name': targetname,'email': targeteml,'username': Nusrr,'phone_number': targetnum,'biography': targetbio,'external_url': targetext,'chaining_enabled': 'on',},proxies=proxies(),timeout=3).text
    if '"status":"ok"' in swaprequest:
      bot.send_message(usid, f"$ Target Changed From @{targetusername} To @{Nusrr}")
      swaprequestb=requests.post('https://www.instagram.com/api/v1/web/accounts/edit/',headers={'Accept':'*/*','Accept-Encoding':'gzip, deflate, br, zstd','Accept-Language':'en-US,en;q=0.9','Content-Length':'172','Content-Type':'application/x-www-form-urlencoded','Cookie':f'mid=ZoELTQALAAHrrtDs_vxxGxbymHOp; ig_did=AE9A514A-C8E1-4B4D-8B75-F05ECED43315; datr=TQuBZnjQ84czQ1Q5ob4tFEOQ; ig_nrcb=1; ps_n=1; ps_l=1; csrftoken=6okPg9LlUka8srympq3b2MkTVQv37KOz; ds_user_id=4118639383; shbid="2238\0544118639383\0541751821329:01f7788977d1eec85e933ee124dd9b3461ac34281d882bd2443d15907bfd772cb94a44b7"; shbts="1720285329\0544118639383\0541751821329:01f7a6bba876091b1f50bd34e279c91ee872c2ff9db99cc9f27745ae5dd6494cea850148"; sessionid={targetsis}; rur="CLN\0544118639383\0541751892305:01f7a3d7345f1a3005d29d604aef3b77c3f479457a0bca66f2ac3626e5c120ff0cab5a02"; wd=660x679','Origin':'https://www.instagram.com','Priority':'u=1, i','Referer':'https://www.instagram.com/accounts/edit/','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"','Sec-Ch-Ua-Full-Version-List':'"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127", "Google Chrome";v="126.0.6478.127"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Model':'""','Sec-Ch-Ua-Platform':'"Windows"','Sec-Ch-Ua-Platform-Version':'"10.0.0"','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36','X-Asbd-Id':'129477','X-Csrftoken':'6okPg9LlUka8srympq3b2MkTVQv37KOz','X-Ig-App-Id':'936619743392459','X-Ig-Www-Claim':'hmac.AR2weuPJ5Xmx7A2u7KN0U3UkNj8cLYFiJttXq_hBLcASZeSg','X-Instagram-Ajax':'1014711147','X-Requested-With':'XMLHttpRequest',},data={'first_name': targetname,'email': targeteml,'username': targetusername,'phone_number': targetnum,'biography': targetbio,'external_url': targetext,'chaining_enabled': 'on',}).text
      if '"status":"ok"' in swaprequestb:
       bot.send_message(usid, f"$ Changed From @{Nusrr} To @{targetusername}")
    else:
      bot.send_message(usid, f"$ Target Blocked")
      swaprequestb=requests.post('https://www.instagram.com/api/v1/web/accounts/edit/',headers={'Accept':'*/*','Accept-Encoding':'gzip, deflate, br, zstd','Accept-Language':'en-US,en;q=0.9','Content-Length':'172','Content-Type':'application/x-www-form-urlencoded','Cookie':f'mid=ZoELTQALAAHrrtDs_vxxGxbymHOp; ig_did=AE9A514A-C8E1-4B4D-8B75-F05ECED43315; datr=TQuBZnjQ84czQ1Q5ob4tFEOQ; ig_nrcb=1; ps_n=1; ps_l=1; csrftoken=6okPg9LlUka8srympq3b2MkTVQv37KOz; ds_user_id=4118639383; shbid="2238\0544118639383\0541751821329:01f7788977d1eec85e933ee124dd9b3461ac34281d882bd2443d15907bfd772cb94a44b7"; shbts="1720285329\0544118639383\0541751821329:01f7a6bba876091b1f50bd34e279c91ee872c2ff9db99cc9f27745ae5dd6494cea850148"; sessionid={targetsis}; rur="CLN\0544118639383\0541751892305:01f7a3d7345f1a3005d29d604aef3b77c3f479457a0bca66f2ac3626e5c120ff0cab5a02"; wd=660x679','Origin':'https://www.instagram.com','Priority':'u=1, i','Referer':'https://www.instagram.com/accounts/edit/','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"','Sec-Ch-Ua-Full-Version-List':'"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127", "Google Chrome";v="126.0.6478.127"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Model':'""','Sec-Ch-Ua-Platform':'"Windows"','Sec-Ch-Ua-Platform-Version':'"10.0.0"','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36','X-Asbd-Id':'129477','X-Csrftoken':'6okPg9LlUka8srympq3b2MkTVQv37KOz','X-Ig-App-Id':'936619743392459','X-Ig-Www-Claim':'hmac.AR2weuPJ5Xmx7A2u7KN0U3UkNj8cLYFiJttXq_hBLcASZeSg','X-Instagram-Ajax':'1014711147','X-Requested-With':'XMLHttpRequest',},data={'first_name': targetname,'email': targeteml,'username': targetusername,'phone_number': targetnum,'biography': targetbio,'external_url': targetext,'chaining_enabled': 'on',}).text
      if '"status":"ok"' in swaprequestb:
       bot.send_message(usid, f"$ Changed From @{Nusrr} To @{targetusername}")
  def sw():
    global atts
    atts += 1
    swaprequest = requests.post('https://www.instagram.com/api/v1/web/accounts/edit/',headers={'Accept':'*/*','Accept-Encoding':'gzip, deflate, br, zstd','Accept-Language':'en-US,en;q=0.9','Content-Length':'172','Content-Type':'application/x-www-form-urlencoded','Cookie':f'mid=ZoELTQALAAHrrtDs_vxxGxbymHOp; ig_did=AE9A514A-C8E1-4B4D-8B75-F05ECED43315; datr=TQuBZnjQ84czQ1Q5ob4tFEOQ; ig_nrcb=1; ps_n=1; ps_l=1; csrftoken=6okPg9LlUka8srympq3b2MkTVQv37KOz; ds_user_id=4118639383; shbid="2238\0544118639383\0541751821329:01f7788977d1eec85e933ee124dd9b3461ac34281d882bd2443d15907bfd772cb94a44b7"; shbts="1720285329\0544118639383\0541751821329:01f7a6bba876091b1f50bd34e279c91ee872c2ff9db99cc9f27745ae5dd6494cea850148"; sessionid={mainsis}; rur="CLN\0544118639383\0541751892305:01f7a3d7345f1a3005d29d604aef3b77c3f479457a0bca66f2ac3626e5c120ff0cab5a02"; wd=660x679','Origin':'https://www.instagram.com','Priority':'u=1, i','Referer':'https://www.instagram.com/accounts/edit/','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"','Sec-Ch-Ua-Full-Version-List':'"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127", "Google Chrome";v="126.0.6478.127"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Model':'""','Sec-Ch-Ua-Platform':'"Windows"','Sec-Ch-Ua-Platform-Version':'"10.0.0"','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36','X-Asbd-Id':'129477','X-Csrftoken':'6okPg9LlUka8srympq3b2MkTVQv37KOz','X-Ig-App-Id':'936619743392459','X-Ig-Www-Claim':'hmac.AR2weuPJ5Xmx7A2u7KN0U3UkNj8cLYFiJttXq_hBLcASZeSg','X-Instagram-Ajax':'1014711147','X-Requested-With':'XMLHttpRequest',},data={'first_name': mainname,'email': maineml,'username': targetusername,'phone_number': mainnum,'biography': swapbio,'external_url': mainext,'chaining_enabled': 'on',},proxies=proxies(),timeout=3).text
    if '"status":"ok"' in swaprequest:
        try:
            bot.edit_message_text(f"[✓] @{targetusername} Claimed successfully - Main", usid, message_idt)
        except:
            pass
        atts += 50
        print(swaprequest)
        try:
            bot.edit_message_text(f"[✓] @{targetusername} \n[✓] Att 『{atts}』 R/s『{atts//2}』", usid, message_id)
        except:
            pass
    else:
      print(swaprequest)
  def sendhook():
    hook = Webhook('https://discord.com/api/webhooks/1426023490942664727/eaPsqxW0lD3P7e8sA9HJTQENo4h0wjz7Tgmwpnq9A9c5R1dxoVn7ypYXAwbJnUunV0IA')
    shook = Webhook(swapperhok)
    embed = Embed(
      description=f'✓ Transfer Completed Successfully\n\nUsername: @{targetusername}\n\nBy insta : @fc_c & tele : @AboDosr',
      color=0x5CDBF0,)
    embed.set_thumbnail("https://images-ext-1.discordapp.net/external/e9RiaqL-wW-fbL4f9QTCaD_inWvHpi-Qei06gXQN7WA/https/i.ibb.co/C7mtzpt/UU2-Hj-LU-Imgur-ezgif-com-video-to-gif-converter.gif?width=387&height=276")
    minf0=requests.get('https://www.instagram.com/api/v1/accounts/edit/web_form_data/',headers={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9','cookie': 'mid=YQvmcwAEAAFVrBezgjwUhwEQuv3c; ig_did=6C10D114-3B6D-4E5E-9E35-5E808661CBAD; ig_nrcb=1; csrftoken=''SpBpgh1gh2cwHaqEvuAHy8qa3hzVS0X7''; ds_user_id=46165248972; sessionid='+mainsis+';','sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"','sec-ch-ua-mobile': '?0','X-CSRFToken': 'SpBpgh1gh2cwHaqEvuAHy8qa3hzVS0X7  ','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'none','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36','X-ASBD-ID': '198387','X-IG-App-ID':'936619743392459','X-IG-WWW-Claim':'hmac.AR17kjNkBRGeLlBfAI8CoTLRCRKG-JJu19_qw3U1ANoAyjmi','X-Requested-With':'XMLHttpRequest',})
    try:
        binf0=requests.get('https://www.instagram.com/api/v1/accounts/edit/web_form_data/',headers={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9','cookie': 'mid=YQvmcwAEAAFVrBezgjwUhwEQuv3c; ig_did=6C10D114-3B6D-4E5E-9E35-5E808661CBAD; ig_nrcb=1; csrftoken=''SpBpgh1gh2cwHaqEvuAHy8qa3hzVS0X7''; ds_user_id=46165248972; sessionid='+bmainsis+';','sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"','sec-ch-ua-mobile': '?0','X-CSRFToken': 'SpBpgh1gh2cwHaqEvuAHy8qa3hzVS0X7  ','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'none','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36','X-ASBD-ID': '198387','X-IG-App-ID':'936619743392459','X-IG-WWW-Claim':'hmac.AR17kjNkBRGeLlBfAI8CoTLRCRKG-JJu19_qw3U1ANoAyjmi','X-Requested-With':'XMLHttpRequest',})
    except:
        binf0 = None

    if targetusername in str(minf0.json()['form_data']['username']):
      hook.send(embed=embed)
      shook.send(embed=embed)
      send_swap_notification(targetusername)
    elif binf0 and targetusername in str(binf0.json()['form_data']['username']):
      hook.send(embed=embed)
      shook.send(embed=embed)
      send_swap_notification(targetusername)
    else:
      print("notswap")
  def bk():
    global atts
    time.sleep(1)
    if bmainsis:
      for i in range(10):
        swaprequest = requests.post('https://www.instagram.com/api/v1/web/accounts/edit/',headers={'Accept':'*/*','Accept-Encoding':'gzip, deflate, br, zstd','Accept-Language':'en-US,en;q=0.9','Content-Length':'172','Content-Type':'application/x-www-form-urlencoded','Cookie':f'mid=ZoELTQALAAHrrtDs_vxxGxbymHOp; ig_did=AE9A514A-C8E1-4B4D-8B75-F05ECED43315; datr=TQuBZnjQ84czQ1Q5ob4tFEOQ; ig_nrcb=1; ps_n=1; ps_l=1; csrftoken=6okPg9LlUka8srympq3b2MkTVQv37KOz; ds_user_id=4118639383; shbid="2238\0544118639383\0541751821329:01f7788977d1eec85e933ee124dd9b3461ac34281d882bd2443d15907bfd772cb94a44b7"; shbts="1720285329\0544118639383\0541751821329:01f7a6bba876091b1f50bd34e279c91ee872c2ff9db99cc9f27745ae5dd6494cea850148"; sessionid={bmainsis}; rur="CLN\0544118639383\0541751892305:01f7a3d7345f1a3005d29d604aef3b77c3f479457a0bca66f2ac3626e5c120ff0cab5a02"; wd=660x679','Origin':'https://www.instagram.com','Priority':'u=1, i','Referer':'https://www.instagram.com/accounts/edit/','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"','Sec-Ch-Ua-Full-Version-List':'"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127", "Google Chrome";v="126.0.6478.127"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Model':'""','Sec-Ch-Ua-Platform':'"Windows"','Sec-Ch-Ua-Platform-Version':'"10.0.0"','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36','X-Asbd-Id':'129477','X-Csrftoken':'6okPg9LlUka8srympq3b2MkTVQv37KOz','X-Ig-App-Id':'936619743392459','X-Ig-Www-Claim':'hmac.AR2weuPJ5Xmx7A2u7KN0U3UkNj8cLYFiJttXq_hBLcASZeSg','X-Instagram-Ajax':'1014711147','X-Requested-With':'XMLHttpRequest',},data={'first_name': bmainname,'email': bmaineml,'username': targetusername,'phone_number': bmainnum,'biography': swapbio,'external_url': bmainext,'chaining_enabled': 'on',},proxies=proxies(),timeout=3).text
        if '"status":"ok"' in swaprequest:
            try:
                bot.edit_message_text(f"[✓] @{targetusername} Claimed successfully - Backup", usid, message_idt)
            except:
                pass
            atts += 50
            print(swaprequest)
            try:
                bot.edit_message_text(f"[✓] @{targetusername} \n[💲] Att『{atts}』 R/s『{atts//2}』", usid, message_id)
            except:
                pass
        else:
            print('swaprequest')
  message = bot.send_message(usid, "[⟲] Swap Operation has Begun")
  messaget = bot.send_message(usid, "[⟲] Backup Process Initiated")
  message_id = message.message_id
  message_idt = messaget.message_id
  threading.Thread(target=fk).start()
  threading.Thread(target=bk).start()
  while atts < 50:
    time.sleep(0.2)
    threading.Thread(target=sw).start()
  sendhook()

def swap():
  global att
  att = 1
  def fk():
    time.sleep(1)
    Nusry = random.randrange(1111,9999)
    Nusryy = random.randrange(1111,9999)
    Nusrr = f"{Nusry}sguu{Nusryy}"
    swaprequest = requests.post('https://www.instagram.com/api/v1/web/accounts/edit/',headers={'Accept':'*/*','Accept-Encoding':'gzip, deflate, br, zstd','Accept-Language':'en-US,en;q=0.9','Content-Length':'172','Content-Type':'application/x-www-form-urlencoded','Cookie':f'mid=ZoELTQALAAHrrtDs_vxxGxbymHOp; ig_did=AE9A514A-C8E1-4B4D-8B75-F05ECED43315; datr=TQuBZnjQ84czQ1Q5ob4tFEOQ; ig_nrcb=1; ps_n=1; ps_l=1; csrftoken=6okPg9LlUka8srympq3b2MkTVQv37KOz; ds_user_id=4118639383; shbid="2238\0544118639383\0541751821329:01f7788977d1eec85e933ee124dd9b3461ac34281d882bd2443d15907bfd772cb94a44b7"; shbts="1720285329\0544118639383\0541751821329:01f7a6bba876091b1f50bd34e279c91ee872c2ff9db99cc9f27745ae5dd6494cea850148"; sessionid={targetsis}; rur="CLN\0544118639383\0541751892305:01f7a3d7345f1a3005d29d604aef3b77c3f479457a0bca66f2ac3626e5c120ff0cab5a02"; wd=660x679','Origin':'https://www.instagram.com','Priority':'u=1, i','Referer':'https://www.instagram.com/accounts/edit/','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"','Sec-Ch-Ua-Full-Version-List':'"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127", "Google Chrome";v="126.0.6478.127"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Model':'""','Sec-Ch-Ua-Platform':'"Windows"','Sec-Ch-Ua-Platform-Version':'"10.0.0"','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36','X-Asbd-Id':'129477','X-Csrftoken':'6okPg9LlUka8srympq3b2MkTVQv37KOz','X-Ig-App-Id':'936619743392459','X-Ig-Www-Claim':'hmac.AR2weuPJ5Xmx7A2u7KN0U3UkNj8cLYFiJttXq_hBLcASZeSg','X-Instagram-Ajax':'1014711147','X-Requested-With':'XMLHttpRequest',},data={'first_name': targetname,'email': targeteml,'username': Nusrr,'phone_number': targetnum,'biography': targetbio,'external_url': targetext,'chaining_enabled': 'on',}).text
    if '"status":"ok"' in swaprequest:
      bot.send_message(usid, f"$ Target Changed From @{targetusername} To @{Nusrr}")
      swaprequestb=requests.post('https://www.instagram.com/api/v1/web/accounts/edit/',headers={'Accept':'*/*','Accept-Encoding':'gzip, deflate, br, zstd','Accept-Language':'en-US,en;q=0.9','Content-Length':'172','Content-Type':'application/x-www-form-urlencoded','Cookie':f'mid=ZoELTQALAAHrrtDs_vxxGxbymHOp; ig_did=AE9A514A-C8E1-4B4D-8B75-F05ECED43315; datr=TQuBZnjQ84czQ1Q5ob4tFEOQ; ig_nrcb=1; ps_n=1; ps_l=1; csrftoken=6okPg9LlUka8srympq3b2MkTVQv37KOz; ds_user_id=4118639383; shbid="2238\0544118639383\0541751821329:01f7788977d1eec85e933ee124dd9b3461ac34281d882bd2443d15907bfd772cb94a44b7"; shbts="1720285329\0544118639383\0541751821329:01f7a6bba876091b1f50bd34e279c91ee872c2ff9db99cc9f27745ae5dd6494cea850148"; sessionid={targetsis}; rur="CLN\0544118639383\0541751892305:01f7a3d7345f1a3005d29d604aef3b77c3f479457a0bca66f2ac3626e5c120ff0cab5a02"; wd=660x679','Origin':'https://www.instagram.com','Priority':'u=1, i','Referer':'https://www.instagram.com/accounts/edit/','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"','Sec-Ch-Ua-Full-Version-List':'"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127", "Google Chrome";v="126.0.6478.127"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Model':'""','Sec-Ch-Ua-Platform':'"Windows"','Sec-Ch-Ua-Platform-Version':'"10.0.0"','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36','X-Asbd-Id':'129477','X-Csrftoken':'6okPg9LlUka8srympq3b2MkTVQv37KOz','X-Ig-App-Id':'936619743392459','X-Ig-Www-Claim':'hmac.AR2weuPJ5Xmx7A2u7KN0U3UkNj8cLYFiJttXq_hBLcASZeSg','X-Instagram-Ajax':'1014711147','X-Requested-With':'XMLHttpRequest',},data={'first_name': targetname,'email': targeteml,'username': targetusername,'phone_number': targetnum,'biography': targetbio,'external_url': targetext,'chaining_enabled': 'on',}).text
      if '"status":"ok"' in swaprequestb:
       bot.send_message(usid, f"$ Changed From @{Nusrr} To @{targetusername}")
    else:
      bot.send_message(usid, f"$ Target Blocked")
  def sw():
    global att
    att += 1
    swaprequest = requests.post('https://www.instagram.com/api/v1/web/accounts/edit/',headers={'Accept':'*/*','Accept-Encoding':'gzip, deflate, br, zstd','Accept-Language':'en-US,en;q=0.9','Content-Length':'172','Content-Type':'application/x-www-form-urlencoded','Cookie':f'mid=ZoELTQALAAHrrtDs_vxxGxbymHOp; ig_did=AE9A514A-C8E1-4B4D-8B75-F05ECED43315; datr=TQuBZnjQ84czQ1Q5ob4tFEOQ; ig_nrcb=1; ps_n=1; ps_l=1; csrftoken=6okPg9LlUka8srympq3b2MkTVQv37KOz; ds_user_id=4118639383; shbid="2238\0544118639383\0541751821329:01f7788977d1eec85e933ee124dd9b3461ac34281d882bd2443d15907bfd772cb94a44b7"; shbts="1720285329\0544118639383\0541751821329:01f7a6bba876091b1f50bd34e279c91ee872c2ff9db99cc9f27745ae5dd6494cea850148"; sessionid={mainsis}; rur="CLN\0544118639383\0541751892305:01f7a3d7345f1a3005d29d604aef3b77c3f479457a0bca66f2ac3626e5c120ff0cab5a02"; wd=660x679','Origin':'https://www.instagram.com','Priority':'u=1, i','Referer':'https://www.instagram.com/accounts/edit/','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"','Sec-Ch-Ua-Full-Version-List':'"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127", "Google Chrome";v="126.0.6478.127"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Model':'""','Sec-Ch-Ua-Platform':'"Windows"','Sec-Ch-Ua-Platform-Version':'"10.0.0"','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36','X-Asbd-Id':'129477','X-Csrftoken':'6okPg9LlUka8srympq3b2MkTVQv37KOz','X-Ig-App-Id':'936619743392459','X-Ig-Www-Claim':'hmac.AR2weuPJ5Xmx7A2u7KN0U3UkNj8cLYFiJttXq_hBLcASZeSg','X-Instagram-Ajax':'1014711147','X-Requested-With':'XMLHttpRequest',},data={'first_name': mainname,'email': maineml,'username': targetusername,'phone_number': mainnum,'biography': swapbio,'external_url': mainext,'chaining_enabled': 'on',}).text
    if '"status":"ok"' in swaprequest:
        try:
            bot.edit_message_text(f"[✓] @{targetusername} Claimed successfully - Main", usid, message_idt)
        except:
            pass
        att += 50
        print(swaprequest)
        try:
            bot.edit_message_text(f"[✓] @{targetusername} \n[✓] Att 『{att}』 R/s『{att//2}』", usid, message_id)
        except:
            pass
    else:
      print(swaprequest)
  def bk():
    global att
    time.sleep(1)
    if bmainsis:
      for i in range(10):
        swaprequest = requests.post('https://www.instagram.com/api/v1/web/accounts/edit/',headers={'Accept':'*/*','Accept-Encoding':'gzip, deflate, br, zstd','Accept-Language':'en-US,en;q=0.9','Content-Length':'172','Content-Type':'application/x-www-form-urlencoded','Cookie':f'mid=ZoELTQALAAHrrtDs_vxxGxbymHOp; ig_did=AE9A514A-C8E1-4B4D-8B75-F05ECED43315; datr=TQuBZnjQ84czQ1Q5ob4tFEOQ; ig_nrcb=1; ps_n=1; ps_l=1; csrftoken=6okPg9LlUka8srympq3b2MkTVQv37KOz; ds_user_id=4118639383; shbid="2238\0544118639383\0541751821329:01f7788977d1eec85e933ee124dd9b3461ac34281d882bd2443d15907bfd772cb94a44b7"; shbts="1720285329\0544118639383\0541751821329:01f7a6bba876091b1f50bd34e279c91ee872c2ff9db99cc9f27745ae5dd6494cea850148"; sessionid={bmainsis}; rur="CLN\0544118639383\0541751892305:01f7a3d7345f1a3005d29d604aef3b77c3f479457a0bca66f2ac3626e5c120ff0cab5a02"; wd=660x679','Origin':'https://www.instagram.com','Priority':'u=1, i','Referer':'https://www.instagram.com/accounts/edit/','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"','Sec-Ch-Ua-Full-Version-List':'"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127", "Google Chrome";v="126.0.6478.127"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Model':'""','Sec-Ch-Ua-Platform':'"Windows"','Sec-Ch-Ua-Platform-Version':'"10.0.0"','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36','X-Asbd-Id':'129477','X-Csrftoken':'6okPg9LlUka8srympq3b2MkTVQv37KOz','X-Ig-App-Id':'936619743392459','X-Ig-Www-Claim':'hmac.AR2weuPJ5Xmx7A2u7KN0U3UkNj8cLYFiJttXq_hBLcASZeSg','X-Instagram-Ajax':'1014711147','X-Requested-With':'XMLHttpRequest',},data={'first_name': bmainname,'email': bmaineml,'username': targetusername,'phone_number': bmainnum,'biography': swapbio,'external_url': bmainext,'chaining_enabled': 'on',}).text
        if '"status":"ok"' in swaprequest:
            try:
                bot.edit_message_text(f"[✓] @{targetusername} Claimed successfully - Backup", usid, message_idt)
            except:
                pass
            att += 50
            print(swaprequest)
            try:
                bot.edit_message_text(f"[✓] @{targetusername} \n$ Att『{att}』 R/s『{att//2}』", usid, message_id)
            except:
                pass
        else:
            print('swaprequest')
  def sendhook():
    hook = Webhook('https://discord.com/api/webhooks/1426023490942664727/eaPsqxW0lD3P7e8sA9HJTQENo4h0wjz7Tgmwpnq9A9c5R1dxoVn7ypYXAwbJnUunV0IA')
    shook = Webhook(swapperhok)
    embed = Embed(
      description=f'✓ Transfer Completed Successfully\n\nUsername: @{targetusername}\n\nBy insta : @fc_c & tele : @AboDosr',
      color=0x5CDBF0,)
    embed.set_thumbnail("https://images-ext-1.discordapp.net/external/e9RiaqL-wW-fbL4f9QTCaD_inWvHpi-Qei06gXQN7WA/https/i.ibb.co/C7mtzpt/UU2-Hj-LU-Imgur-ezgif-com-video-to-gif-converter.gif?width=387&height=276")
    minf0=requests.get('https://www.instagram.com/api/v1/accounts/edit/web_form_data/',headers={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9','cookie': 'mid=YQvmcwAEAAFVrBezgjwUhwEQuv3c; ig_did=6C10D114-3B6D-4E5E-9E35-5E808661CBAD; ig_nrcb=1; csrftoken=''SpBpgh1gh2cwHaqEvuAHy8qa3hzVS0X7''; ds_user_id=46165248972; sessionid='+mainsis+';','sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"','sec-ch-ua-mobile': '?0','X-CSRFToken': 'SpBpgh1gh2cwHaqEvuAHy8qa3hzVS0X7  ','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'none','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36','X-ASBD-ID': '198387','X-IG-App-ID':'936619743392459','X-IG-WWW-Claim':'hmac.AR17kjNkBRGeLlBfAI8CoTLRCRKG-JJu19_qw3U1ANoAyjmi','X-Requested-With':'XMLHttpRequest',})
    try:
        binf0=requests.get('https://www.instagram.com/api/v1/accounts/edit/web_form_data/',headers={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9','cookie': 'mid=YQvmcwAEAAFVrBezgjwUhwEQuv3c; ig_did=6C10D114-3B6D-4E5E-9E35-5E808661CBAD; ig_nrcb=1; csrftoken=''SpBpgh1gh2cwHaqEvuAHy8qa3hzVS0X7''; ds_user_id=46165248972; sessionid='+bmainsis+';','sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"','sec-ch-ua-mobile': '?0','X-CSRFToken': 'SpBpgh1gh2cwHaqEvuAHy8qa3hzVS0X7  ','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'none','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36','X-ASBD-ID': '198387','X-IG-App-ID':'936619743392459','X-IG-WWW-Claim':'hmac.AR17kjNkBRGeLlBfAI8CoTLRCRKG-JJu19_qw3U1ANoAyjmi','X-Requested-With':'XMLHttpRequest',})
    except:
        binf0 = None

    if targetusername in str(minf0.json()['form_data']['username']):
      hook.send(embed=embed)
      shook.send(embed=embed)
      send_swap_notification(targetusername)
    elif binf0 and targetusername in str(binf0.json()['form_data']['username']):
      hook.send(embed=embed)
      shook.send(embed=embed)
      send_swap_notification(targetusername)
    else:
      print("notswap")
  message = bot.send_message(usid, "{⟲} Swap Started")
  messaget = bot.send_message(usid, "{⟲} backup Started")
  message_id = message.message_id
  message_idt = messaget.message_id
  threading.Thread(target=fk).start()
  threading.Thread(target=bk).start()
  while att < 50:
    time.sleep(0.2)
    threading.Thread(target=sw).start()
  sendhook()

def tthreads(message):
  global Tthreads
  Tthreads = message.text
  bot.send_message(message.chat.id, f"$ Threads {Tthreads}")

def targetinfo(message):
  global targetsis,targetname,targetext,targeteml,targetbio,targetnum,targetusername
  targetsis = message.text
  inf0=requests.get('https://www.instagram.com/api/v1/accounts/edit/web_form_data/',headers={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9','cookie': 'mid=YQvmcwAEAAFVrBezgjwUhwEQuv3c; ig_did=6C10D114-3B6D-4E5E-9E35-5E808661CBAD; ig_nrcb=1; csrftoken=''SpBpgh1gh2cwHaqEvuAHy8qa3hzVS0X7''; ds_user_id=46165248972; sessionid='+targetsis+';','sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"','sec-ch-ua-mobile': '?0','X-CSRFToken': 'SpBpgh1gh2cwHaqEvuAHy8qa3hzVS0X7  ','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'none','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36','X-ASBD-ID': '198387','X-IG-App-ID':'936619743392459','X-IG-WWW-Claim':'hmac.AR17kjNkBRGeLlBfAI8CoTLRCRKG-JJu19_qw3U1ANoAyjmi','X-Requested-With':'XMLHttpRequest',})
  try:
        targetusername=str(inf0.json()['form_data']['username'])
        targetname=str(inf0.json()['form_data']['first_name'])
        targetext=str(inf0.json()['form_data']['external_url'])
        targeteml=str(inf0.json()['form_data']['email'])
        targetbio=str(inf0.json()['form_data']['biography'])
        targetnum=str(inf0.json()['form_data']['phone_number'])
        bot.send_message(message.chat.id, f"$ The Account UserName is @{targetusername}")
  except Exception as e:
        bot.send_message(message.chat.id, "$ The Sessionid is wrong ")

def maininfo(message):
  global mainsis,mainname,mainext,maineml,mainbio,mainnum
  mainsis = message.text
  inf0=requests.get('https://www.instagram.com/api/v1/accounts/edit/web_form_data/',headers={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9','cookie': 'mid=YQvmcwAEAAFVrBezgjwUhwEQuv3c; ig_did=6C10D114-3B6D-4E5E-9E35-5E808661CBAD; ig_nrcb=1; csrftoken=''SpBpgh1gh2cwHaqEvuAHy8qa3hzVS0X7''; ds_user_id=46165248972; sessionid='+mainsis+';','sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"','sec-ch-ua-mobile': '?0','X-CSRFToken': 'SpBpgh1gh2cwHaqEvuAHy8qa3hzVS0X7  ','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'none','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36','X-ASBD-ID': '198387','X-IG-App-ID':'936619743392459','X-IG-WWW-Claim':'hmac.AR17kjNkBRGeLlBfAI8CoTLRCRKG-JJu19_qw3U1ANoAyjmi','X-Requested-With':'XMLHttpRequest',})
  try:
        mainusername=str(inf0.json()['form_data']['username'])
        mainname=str(inf0.json()['form_data']['first_name'])
        mainext=str(inf0.json()['form_data']['external_url'])
        maineml=str(inf0.json()['form_data']['email'])
        mainbio=str(inf0.json()['form_data']['biography'])
        mainnum=str(inf0.json()['form_data']['phone_number'])
        bot.send_message(message.chat.id, f"$ The Account UserName is @{mainusername}")
  except Exception as e:
        bot.send_message(message.chat.id, "$ The Sessionid is wrong ")
  Nusry = random.randrange(1111,9999)
  Nusryy = random.randrange(1111,9999)
  Nusrr = f"{Nusry}sguu{Nusryy}"
  swaprequest = requests.post('https://www.instagram.com/api/v1/web/accounts/edit/',headers={'Accept':'*/*','Accept-Encoding':'gzip, deflate, br, zstd','Accept-Language':'en-US,en;q=0.9','Content-Length':'172','Content-Type':'application/x-www-form-urlencoded','Cookie':f'mid=ZoELTQALAAHrrtDs_vxxGxbymHOp; ig_did=AE9A514A-C8E1-4B4D-8B75-F05ECED43315; datr=TQuBZnjQ84czQ1Q5ob4tFEOQ; ig_nrcb=1; ps_n=1; ps_l=1; csrftoken=6okPg9LlUka8srympq3b2MkTVQv37KOz; ds_user_id=4118639383; shbid="2238\0544118639383\0541751821329:01f7788977d1eec85e933ee124dd9b3461ac34281d882bd2443d15907bfd772cb94a44b7"; shbts="1720285329\0544118639383\0541751821329:01f7a6bba876091b1f50bd34e279c91ee872c2ff9db99cc9f27745ae5dd6494cea850148"; sessionid={mainsis}; rur="CLN\0544118639383\0541751892305:01f7a3d7345f1a3005d29d604aef3b77c3f479457a0bca66f2ac3626e5c120ff0cab5a02"; wd=660x679','Origin':'https://www.instagram.com','Priority':'u=1, i','Referer':'https://www.instagram.com/accounts/edit/','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"','Sec-Ch-Ua-Full-Version-List':'"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127", "Google Chrome";v="126.0.6478.127"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Model':'""','Sec-Ch-Ua-Platform':'"Windows"','Sec-Ch-Ua-Platform-Version':'"10.0.0"','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36','X-Asbd-Id':'129477','X-Csrftoken':'6okPg9LlUka8srympq3b2MkTVQv37KOz','X-Ig-App-Id':'936619743392459','X-Ig-Www-Claim':'hmac.AR2weuPJ5Xmx7A2u7KN0U3UkNj8cLYFiJttXq_hBLcASZeSg','X-Instagram-Ajax':'1014711147','X-Requested-With':'XMLHttpRequest',},data={'first_name': mainname,'email': maineml,'username': Nusrr,'phone_number': mainnum,'biography': mainbio,'external_url': mainext,'chaining_enabled': 'on',}).text
  if '"status":"ok"' in swaprequest:
    bot.send_message(usid, f"$ Main: Good Check @{Nusrr}")
  else:
    bot.send_message(usid, f"$ Main Blocked")

def bkinfo(message):
  global bmainsis,bmainname,bmainext,bmaineml,bmainbio,bmainnum
  bmainsis = message.text
  inf0=requests.get('https://www.instagram.com/api/v1/accounts/edit/web_form_data/',headers={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9','cookie': 'mid=YQvmcwAEAAFVrBezgjwUhwEQuv3c; ig_did=6C10D114-3B6D-4E5E-9E35-5E808661CBAD; ig_nrcb=1; csrftoken=''SpBpgh1gh2cwHaqEvuAHy8qa3hzVS0X7''; ds_user_id=46165248972; sessionid='+bmainsis+';','sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"','sec-ch-ua-mobile': '?0','X-CSRFToken': 'SpBpgh1gh2cwHaqEvuAHy8qa3hzVS0X7  ','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'none','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36','X-ASBD-ID': '198387','X-IG-App-ID':'936619743392459','X-IG-WWW-Claim':'hmac.AR17kjNkBRGeLlBfAI8CoTLRCRKG-JJu19_qw3U1ANoAyjmi','X-Requested-With':'XMLHttpRequest',})
  try:
        bmainusername=str(inf0.json()['form_data']['username'])
        bmainname=str(inf0.json()['form_data']['first_name'])
        bmainext=str(inf0.json()['form_data']['external_url'])
        bmaineml=str(inf0.json()['form_data']['email'])
        bmainbio=str(inf0.json()['form_data']['biography'])
        bmainnum=str(inf0.json()['form_data']['phone_number'])
        bot.send_message(message.chat.id, f"$ The Account UserName is @{bmainusername}")
  except Exception as e:
        bot.send_message(message.chat.id, "$ The Sessionid is wrong ")
  Nusry = random.randrange(1111,9999)
  Nusryy = random.randrange(1111,9999)
  Nusrr = f"{Nusry}sguu{Nusryy}"
  swaprequest = requests.post('https://www.instagram.com/api/v1/web/accounts/edit/',headers={'Accept':'*/*','Accept-Encoding':'gzip, deflate, br, zstd','Accept-Language':'en-US,en;q=0.9','Content-Length':'172','Content-Type':'application/x-www-form-urlencoded','Cookie':f'mid=ZoELTQALAAHrrtDs_vxxGxbymHOp; ig_did=AE9A514A-C8E1-4B4D-8B75-F05ECED43315; datr=TQuBZnjQ84czQ1Q5ob4tFEOQ; ig_nrcb=1; ps_n=1; ps_l=1; csrftoken=6okPg9LlUka8srympq3b2MkTVQv37KOz; ds_user_id=4118639383; shbid="2238\0544118639383\0541751821329:01f7788977d1eec85e933ee124dd9b3461ac34281d882bd2443d15907bfd772cb94a44b7"; shbts="1720285329\0544118639383\0541751821329:01f7a6bba876091b1f50bd34e279c91ee872c2ff9db99cc9f27745ae5dd6494cea850148"; sessionid={bmainsis}; rur="CLN\0544118639383\0541751892305:01f7a3d7345f1a3005d29d604aef3b77c3f479457a0bca66f2ac3626e5c120ff0cab5a02"; wd=660x679','Origin':'https://www.instagram.com','Priority':'u=1, i','Referer':'https://www.instagram.com/accounts/edit/','Sec-Ch-Prefers-Color-Scheme':'dark','Sec-Ch-Ua':'"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"','Sec-Ch-Ua-Full-Version-List':'"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.127", "Google Chrome";v="126.0.6478.127"','Sec-Ch-Ua-Mobile':'?0','Sec-Ch-Ua-Model':'""','Sec-Ch-Ua-Platform':'"Windows"','Sec-Ch-Ua-Platform-Version':'"10.0.0"','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36','X-Asbd-Id':'129477','X-Csrftoken':'6okPg9LlUka8srympq3b2MkTVQv37KOz','X-Ig-App-Id':'936619743392459','X-Ig-Www-Claim':'hmac.AR2weuPJ5Xmx7A2u7KN0U3UkNj8cLYFiJttXq_hBLcASZeSg','X-Instagram-Ajax':'1014711147','X-Requested-With':'XMLHttpRequest',},data={'first_name': bmainname,'email': bmaineml,'username': Nusrr,'phone_number': bmainnum,'biography': bmainbio,'external_url': bmainext,'chaining_enabled': 'on',}).text
  if '"status":"ok"' in swaprequest:
    bot.send_message(usid, f"$ backup: Good Check @{Nusrr}")
  else:
    bot.send_message(usid, f"$ backup Blocked")

def namehqoq(message):
  global swappername
  swappername = message.text
  bot.send_message(message.chat.id, f"$ {message.text}")

def swaperprx(message):
  global swapperproxies
  swapperproxies = message.text
  bot.send_message(usid, f"$ {message.text}")

def chprx():
  try:
    response = requests.get("http://httpbin.org/ip", proxies=proxies())
    bot.send_message(usid, f"$ Good Proxie ({response.json()})")
    swapprx()
  except requests.exceptions.RequestException as e:
     bot.send_message(usid, f"$ Bad Proxie")

def swaphook(message):
  global swapperhok
  swapperhok = message.text
  bot.send_message(message.chat.id, f"$ Done")


bot.infinity_polling()
