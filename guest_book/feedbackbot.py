import telebot
import settings
import redis
import json
import time

bot = telebot.TeleBot(settings.feedbackbot_token)

queue = redis.StrictRedis(host='localhost', port=6379, db=0)
channel = queue.pubsub()
     
@bot.message_handler(commands =['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, я бот для получекния фидбэка, напиши мне свое мнение!')

@bot.message_handler(content_types = ["text"])   
def place(message):
    try:
        user_name = message.from_user.first_name + ' [From Telegram]'
    except:
        user_name = 'Anonymous [From Telegram]'
    tim = time.asctime()
    text = message.text

    data = str({"name":user_name, "time":tim, "text":text})
    queue.publish('channel', data)
    
    bot.send_message(message.chat.id, 'Ваш ответ записан, спасибо')

bot.polling()    
