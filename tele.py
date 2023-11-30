import telebot
from telebot import types
from dotenv import load_dotenv
import os
from model import Area, Major, session, Skill, User
from services import insert_skill, match_jd, update

load_dotenv()

API_TOKEN = os.environ.get("TELEGRAM_API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

bot.delete_webhook()



@bot.message_handler(commands=["info"])
def send_info(message):
    user = update(message.chat.id)
    skills = session.query(Skill).filter_by(user=str(message.chat.id)).all()
    resp = f"Thông tin chi tiết:\n1, Ngành nghề : {user.major}\n2, Khu vực: {user.area}\n3, Năm kinh nghiệm: {user.experience} năm\n4, Kĩ năng:\n"
    skill_resp = ""
    for i in range(len(skills)):
        skill_resp +=f"\t- {skills[i].describe}\n"
    resp += skill_resp
    bot.reply_to(message, resp)
    
@bot.message_handler(commands=["experience"])
def send_experience(message):
    try:
        experience = int(message.text.replace("/experience", "").strip())
        update(message.chat.id, experience=experience)
        bot.send_message(message.chat.id, f"Bạn vừa cập nhật số năm kinh nghiệm của mình: {experience} năm")
    except:
        bot.send_message(message.chat.id, "Tin nhắn của bạn có vẻ không đúng cú pháp. Gõ /help để biết thêm chi tiết")

@bot.message_handler(commands=["add_skill"])
def send_add_skill(message):
    try:
        skill = message.text.replace("/add_skill", "").strip()
        if len(skill) > 0:
            insert_skill(message.chat.id, skill)
            bot.send_message(message.chat.id, f"Bạn vừa cập nhật kĩ năng của mình: {skill}")
        else:
            bot.send_message(message.chat.id, "Tin nhắn của bạn có vẻ không đúng cú pháp. Gõ /help để biết thêm chi tiết")
    except:
        bot.send_message(message.chat.id, "Tin nhắn của bạn có vẻ không đúng cú pháp. Gõ /help để biết thêm chi tiết")
        
@bot.message_handler(commands=["remove_skill"])
def choice_remove_skill(message):
    markup = types.InlineKeyboardMarkup()
    skills = session.query(Skill).filter_by(user=str(message.chat.id)).all()
    for skill in skills:
        skill_button = types.InlineKeyboardButton(skill.describe, callback_data=f'skill_{skill.describe}')
        markup.add(skill_button)
    bot.send_message(message.chat.id, "Chọn kĩ năng bạn muốn xóa:", reply_markup=markup)
    
@bot.message_handler(commands=["skills"])
def send_all_skill(message):
    skills = session.query(Skill).filter_by(user=str(message.chat.id)).all()
    resp = "Các kĩ năng bạn đã cập nhật:\n"
    for i in range(len(skills)):
        resp += f"{i + 1}. {skills[i].describe}\n"
    bot.send_message(message.chat.id, resp)

@bot.message_handler(commands=["jd"])
def find_jd(message):
    try:
        jd_num = int(message.text.replace("/jd", "").strip())
        if jd_num <= 0:
            bot.send_message(message.chat.id, "Không tìm thấy công việc nào theo yêu cầu của bạn") 
            return 
        jds = match_jd(message.chat.id, jd_num)
        if len(jds) == 0:
            bot.send_message(message.chat.id, "Không tìm thấy công việc nào theo yêu cầu của bạn") 
            return 
        resp = "Các công việc sau có thể phù hợp với bạn:\n"
        bot.send_message(message.chat.id, resp) 
        for i in range(len(jds)):
            resp = ""
            resp += f"{i + 1}. {jds[i][1].name}\n"
            resp += f"- Công ty: {jds[i][1].company}\n"
            resp += f"- Mô tả công việc: {jds[i][1].describe.replace('-', '').replace(chr(10), '.')}\n"
            resp += f"- Kĩ năng yêu cầu: {jds[i][1].skill}\n"
            resp += f"- Luơng: {jds[i][1].salary}\n"
            resp += f"- Quyền lợi: {jds[i][1].benefit}\n"
            resp += f"- Liên hệ: {jds[i][1].contact}\n"
            bot.send_message(message.chat.id, resp) 
    except:
        bot.send_message(message.chat.id, "Tin nhắn của bạn có vẻ không đúng cú pháp. Gõ /help để biết thêm chi tiết")
        
@bot.message_handler(commands=["help", "start"])
def help(message):
    try:
        resp = """
Bạn có thể ra lệnh cho boJ bằng những lệnh sau:
    Khu vực:
        /area 
    Ngành nghề:
        /major
    Kinh nghiệm:
        /experience <số năm kinh nghiệm>
        Ví dụ: /experience 5
    Kĩ năng:
        /add_skill <mô tả chi tiết kĩ năng>
        Ví dụ /add_skill python
        /skills
        /remove_skill
    Thông tin cá nhân:
        /info 
    Công việc:
        /jd <số công việc bạn muốn boJ đưa ra>
        Ví dụ: /jd 10 
        Lưu ý: Số công việc đưa ra có thể ít hơn số lượng bạn yêu cầu
    Xoá hết dữ liệu:
        /clear
"""
        bot.send_message(message.chat.id, resp)
    except:
        bot.send_message(message.chat.id, "Tin nhắn của bạn có vẻ không đúng cú pháp. Gõ /help để biết thêm chi tiết")

        
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
    bot.send_message(message.chat.id, "Chọn ngành nghề của bạn:", reply_markup=markup)

@bot.message_handler(commands=["clear"])
def clear_data(message):
    try:
        session.query(Skill).filter(Skill.user==str(message.chat.id)).delete()
        session.query(User).filter(User.chat_id == str(message.chat.id)).delete()
        bot.send_message(message.chat.id, f"Bạn đã xóa hết data hiện tại")
    except:
        bot.send_message(message.chat.id, "Tin nhắn của bạn có vẻ không đúng cú pháp. Gõ /help để biết thêm chi tiết")


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
    if choosen[0] == 'skill':
        session.query(Skill).filter(Skill.user == str(call.message.chat.id), Skill.describe == choosen[1]).delete()
        session.commit()
        bot.send_message(call.message.chat.id, f"Bạn đã xóa kĩ năng: {choosen[1]}")

        
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Tin nhắn của bạn có vẻ không đúng cú pháp. Gõ /help để biết thêm chi tiết")
    
bot.polling()
