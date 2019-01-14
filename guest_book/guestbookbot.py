import telebot
from telebot import types
import settings
import redis
import json
import time

bot = telebot.TeleBot(settings.guestbookbot_token)
    
def post(message):
    bot.send_message('@guestbooklaba', message)

r = redis.StrictRedis(host='localhost', port=6379, db=0)
p = r.pubsub()
p.subscribe('channel')

while True:
    message = p.get_message()
    if message and message['data'] != 1:
        data = json.loads(str(message['data'].decode('utf-8')).replace("'", '"'))
        mes = data['name'] + '\n' + data['time'] + '\n\n' + data['text']
        post(mes)

