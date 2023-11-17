import telebot
from telebot import types
from dotenv import load_dotenv
import os
from model import Area, Major, session
from services import update

load_dotenv()

API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

bot.delete_webhook()

# Define a command handler
@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('/info')
    itembtn2 = types.KeyboardButton('/options')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Welcome to YourBot! Choose an option:", reply_markup=markup)

@bot.message_handler(commands=["info"])
def send_info(message):
    user = update(message.chat.id)
    resp = f"""
    Thông tin chi tiết:
    - Ngành nghề : {user.major}
    - Khu vực: {user.area}
    - Năm kinh nghiệm: {user.experience} năm
    """
    bot.reply_to(message, resp)
    
@bot.message_handler(commands=["experience"])
def send_welcome(message):
    try:
        experience = int(message.text.replace("/experience", "").strip())
        update(message.chat.id, experience=experience)
        bot.send_message(message.chat.id, f"Bạn vừa cập nhật số năm kinh nghiệm của mình: {experience} năm")
    except:
        bot.send_message(message.chat.id, "Sai cú pháp")
        
@bot.message_handler(commands=["area"])
def send_area_options(message):
    markup = types.InlineKeyboardMarkup()
    areas = session.query(Area).all()
    for area in areas:
        area_button = types.InlineKeyboardButton(area.name, callback_data=f'area_{area.name}')
        markup.add(area_button)
    bot.send_message(message.chat.id, "Chọn khu vực của bạn:", reply_markup=markup)

@bot.message_handler(commands=["major"])
def send_area_options(message):
    markup = types.InlineKeyboardMarkup()
    majors = session.query(Major).all()
    for major in majors:
        area_button = types.InlineKeyboardButton(major.name, callback_data=f'major_{major.name}')
        markup.add(area_button)
    bot.send_message(message.chat.id, "Chọn ngành nghề  của bạn:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print(call.data)
    print(call.message.chat.id)
    choosen = call.data.split('_')
    if choosen[0] == 'area':
        update(call.message.chat.id, area=choosen[1])
        bot.send_message(call.message.chat.id, f"Bạn đã chọn khu vực: {choosen[1]}")
    if choosen[0] == 'major':
        update(call.message.chat.id, major=choosen[1])
        bot.send_message(call.message.chat.id, f"Bạn đã chọn ngành nghề: {choosen[1]}")

bot.polling()
