import telebot
from telebot import types
import settings 
import time
import json

bot = telebot.TeleBot(settings.guestbookbot_token)

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
    
def post(message):
    bot.send_message('@guestbooklaba', message)

while True:
    users_data = read_users_data(settings.users_data_file_link)
    if users_data['data'] != []:
        diction = users_data['data'].pop()
        mes = diction['name'] + '\n' + diction['time'] + '\n\n' + diction['text']
        post(mes)
        write_users_data(users_data, settings.users_data_file_link)
    time.sleep(1)
    

bot.polling()
