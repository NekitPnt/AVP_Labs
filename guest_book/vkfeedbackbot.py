import requests
import settings
import json
import time

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType

start_array = ['начать', 'старт']

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

def place(event):
    users_data = read_users_data(settings.users_data_file_link)
    try:
        user_name = vk.users.get(access_token=settings.vkfeedbackbot_token, user_ids=event.user_id)[0]['first_name']
    except:
        user_name = 'Anonymous'
    tim = time.asctime()
    text = event.text
    users_data['data'].append({"name":user_name, "time":tim, "text":text})
    write_users_data(users_data, settings.users_data_file_link)

    vk.messages.send(user_id=event.user_id, random_id=0, message='Ваш ответ записан, спасибо')

session = requests.Session()
vk_session = vk_api.VkApi(token=settings.vkfeedbackbot_token)
    
vk = vk_session.get_api()

longpoll = VkLongPoll(vk_session)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.text.lower() in start_array:
            vk.messages.send(user_id=event.user_id, random_id=0, message='Привет, я бот для получекния фидбэка, напиши мне свое мнение!')
        else:
            place(event)





'''import json
import settings


import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def main():
    """ Пример использования bots longpoll
        https://vk.com/dev/bots_longpoll
    """

    vk_session = vk_api.VkApi(token=settings.vkfeedbackbot_token)

    longpoll = VkBotLongPoll(vk_session, 'your_group_id')

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            print('Новое сообщение:')

            print('Для меня от: ', end='')

            print(event.obj.from_id)

            print('Текст:', event.obj.text)
            print()

        elif event.type == VkBotEventType.MESSAGE_REPLY:
            print('Новое сообщение:')

            print('От меня для: ', end='')

            print(event.obj.peer_id)

            print('Текст:', event.obj.text)
            print()

        elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            print('Печатает ', end='')

            print(event.obj.from_id, end=' ')

            print('для ', end='')

            print(event.obj.to_id)
            print()

        elif event.type == VkBotEventType.GROUP_JOIN:
            print(event.obj.user_id, end=' ')

            print('Вступил в группу!')
            print()

        elif event.type == VkBotEventType.GROUP_LEAVE:
            print(event.obj.user_id, end=' ')

            print('Покинул группу!')
            print()

        else:
            print(event.type)
            print()


if __name__ == '__main__':
main()


session = vk.Session()
api = vk.API(session, v=5.50)

def send_message(token, user_id, message="", attachment=""):
    api.messages.send(access_token=token, user_id=str(user_id),
        message=message, attachment=attachment)

def get_user(token, user_id):
    #[{'id': id, 'first_name': 'Name', 'last_name': 'Lname'}]
    user = api.users.get(access_token=token, user_ids=user_id)[0]
    return user['first_name'], user['last_name']

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



while True:
    main.create_answer(data['object'], token)
    '''
