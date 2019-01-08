import telebot
from telebot import types
import settings 
import time
import json

bot = telebot.TeleBot(settings.feedbackbot_token)

def write_users_data(data, link):
    with open(link, 'w') as outfile:
        json.dump(data, outfile, indent = 4, ensure_ascii = False)

def read_users_data(link):
    try:
        read_file = open(link, "r")
    except IOError as e:
        with open(link, "w") as read_file:
            json.dump({'test': 'test'}, read_file, indent = 4, ensure_ascii = False)
    else:
        with read_file:
            data = json.load(read_file)
        return data
        
@bot.message_handler(commands =['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, я бот для получекния фидбэка, напиши мне свое мнение!')


@bot.message_handler(content_types = ["text"])   
def place(message):
    users_data = read_users_data(settings.users_data_file_link)
    try:
        user_name = message.from_user.first_name
    except:
        user_name = 'Anonymous'
    tim = time.asctime()
    text = message.text
    users_data['data'].append({"name":user_name, "time":tim, "text":text})
    write_users_data(users_data, settings.users_data_file_link)
    
    bot.send_message(message.chat.id, 'Ваш ответ записан, спасибо')

bot.polling()
