import os,certifi
from pyrogram import Client,errors
import telebot
import threading
from telebot import types
import asyncio
from backend import app
from db import database

DB = database()
App = app()
os.environ['SSL_CERT_FILE'] = certifi.where() 
api_id = '24405483'
api_hash = '9214a7069fa94fd78a2f267888073650'
TELEGRAM_TOKEN="6787095243:AAGvNT6PCVOCRh1kQUe-NTqdv4Yma5QM8r8"

allwod_ids=["6818604665", "2095495680"]
admin_id= 6818604665

bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False,num_threads=55,skip_pending=True)
 
@bot.message_handler(commands=['add']) 
def handle_stat(message): 
 sid = message.from_user.id
 if int(sid) != admin_id: return
 try:
  id = message.text.split(" ")[1] 
  allwod_ids.append(str(id)) 
  bot.reply_to(message, text = f"ID {id} added successfully to the admin IDs") 
 except: 
  bot.reply_to(message, text = "No ID Could Be Detected in The Command Message") 
 
@bot.message_handler(commands=['remove']) 
def handle_remove(message): 
    try:
        sid = message.from_user.id
        if int(sid) != admin_id: return
        id = message.text.split(" ")[1] 
        if id in allwod_ids:
            allwod_ids.remove(id) 
            bot.reply_to(message, text=f"ID {id} removed successfully from the admin IDs") 
            print(allwod_ids) 
        else: 
            bot.reply_to(message, text=f"ID {id} is not in the admin IDs list") 
    except: 
        bot.reply_to(message, text="No ID could be detected in the command message") 
 
@bot.message_handler(commands=['start'])
def Admin(message):
    id = message.from_user.id
    if not str(id) in allwod_ids: return
    num = len(DB.accounts())
    AddAccount=types.InlineKeyboardButton("اضافه حساب 🛎",callback_data="AddAccount")
    Accounts=types.InlineKeyboardButton("اكواد حساباتك 🖲",callback_data="Accounts")
    a1=types.InlineKeyboardButton("نقل اعضاء 👤😇",callback_data="a1")
    inline = types.InlineKeyboardMarkup(keyboard=[[a1],[AddAccount],[Accounts]])
    bot.send_message(message.chat.id,f"""*مرحبا بك  👋

اختار انت عاوز اي من الازرار 🔥
تقدر نقل اعضاء لجروبك 🛎
من اي جروب اخر عام  ☄
عدد الحسابات: {num}
Creator : @Anonymous1AV *""",reply_markup=inline ,parse_mode="markdown")

@bot.callback_query_handler(lambda call:True)
def call(call):
    if call.data =="Accounts":
        num = DB.accounts()
        msg=bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=f"حساباتك المسجلة بلكامل : {num}",parse_mode="markdown")
    if call.data =="AddAccount":
        msg=bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="*قوم بارسال الرقم الذي تريد تسليمه مع رمز الدولة الان*📞🎩",parse_mode="markdown")
        bot.register_next_step_handler(msg, AddAccount)
    if call.data =="a1":
        msg=bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="*ابعت رابط الجروب ال نسرق منو *🖲",parse_mode="markdown")
        bot.register_next_step_handler(msg, statement)
def statement(message):
    Fromgrob = message.text
    msg =bot.send_message(chat_id=message.chat.id,text="*ابعت يبني رابط الجروب ال عاوز تضيف فيه*🛎",parse_mode="markdown")
    bot.register_next_step_handler(msg, statement2,Fromgrob)
def statement2(message,Fromgrob):
    Ingrob = message.text
    msg=bot.send_message(chat_id=message.chat.id,text="*استني يبني شوية ⏱*",parse_mode="markdown")
    T = threading.Thread(target=asyncio.run,args=(App.GETuser(Fromgrob,Ingrob),))
    T.start()
    T.join()
    list = T.return_value
    numUser = len(list)
    bot.send_message(message.chat.id,f"""*تم حفظ جميع الاعضاء المتاحه بنجاح *✅

*معلومات عملية النقل 🥸😇

 الاعضاء المتاحه : {numUser} عضو 😋
النقل من  : {Fromgrob} 🎒
النقل الي : {Ingrob} 🧳
مده الفحص : 1 ثانية ⏱

انتظر الي ان تتم العملية 🎩* """ ,parse_mode="markdown")
    T = threading.Thread(target=asyncio.run,args=(App.ADDuser(list,Ingrob,message.chat.id,bot),))
    T.start()
def AddAccount(message):
    try:         
        if "+" in message.text:
            bot.send_message(message.chat.id,"*انتظر جاري الفحص* ⏱",parse_mode="markdown")
            _client = Client("::memory::", in_memory=True,api_id=api_id, api_hash=api_hash,lang_code="ar")
            _client.connect()
            SendCode = _client.send_code(message.text)
            Mas = bot.send_message(message.chat.id,"*أدخل الرمز المرسل إليك 🔏*",parse_mode="markdown")
            bot.register_next_step_handler(Mas, sigin_up,_client,message.text,SendCode.phone_code_hash,message.text)	
        else:
            Mas = bot.send_message(message.chat.id,"*انتظر جاري الفحص* ⏱")
    except Exception as e:
        bot.send_message(message.chat.id,"ERORR : "+e)
def sigin_up(message,_client,phone,hash,name):
    try:
        bot.send_message(message.chat.id,"*انتظر قليلا ⏱*",parse_mode="markdown")
        _client.sign_in(phone, hash, message.text)
        bot.send_message(message.chat.id,"*تم تاكيد الحساب بنجاح ✅ *",parse_mode="markdown")
        ses= _client.export_session_string()
        DB.AddAcount(ses,name,message.chat.id)
    except errors.SessionPasswordNeeded:
        Mas = bot.send_message(message.chat.id,"*أدخل كلمة المرور الخاصة بحسابك 🔐*",parse_mode="markdown")
        bot.register_next_step_handler(Mas, AddPassword,_client,name)	
def AddPassword(message,_client,name):
    try:
        _client.check_password(message.text) 
        ses= _client.export_session_string()
        DB.AddAcount(ses,name,message.chat.id)
        try:
            _client.stop()
        except:
            pass
        bot.send_message(message.chat.id,"*تم تاكيد الحساب بنجاح ✅ *",parse_mode="markdown")
    except Exception as e:
        print(e)
        try:
            _client.stop()
        except:
            pass
        bot.send_message(message.chat.id,f"ERORR : {e} ")
bot.infinity_polling(none_stop=True,timeout=15, long_polling_timeout =15)
