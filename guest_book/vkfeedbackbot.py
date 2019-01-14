import requests
import settings
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import redis
import json
import time

start_array = ['начать', 'старт']

session = requests.Session()
vk_session = vk_api.VkApi(token=settings.vkfeedbackbot_token)    
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

queue = redis.StrictRedis(host='localhost', port=6379, db=0)
channel = queue.pubsub()

def place(event):
    try:
        user_name = vk.users.get(access_token=settings.vkfeedbackbot_token, user_ids=event.user_id)[0]['first_name'] + ' [From VK]'
    except:
        user_name = 'Anonymous From VK'
    tim = time.asctime()
    text = event.text
    
    data = str({"name":user_name, "time":tim, "text":text})
    queue.publish('channel', data)

    vk.messages.send(user_id=event.user_id, random_id=0, message='Ваш ответ записан, спасибо')


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.text.lower() in start_array:
            vk.messages.send(user_id=event.user_id, random_id=0, message='Привет, я бот для получекния фидбэка, напиши мне свое мнение!')
        else:
            place(event)
