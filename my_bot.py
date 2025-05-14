import os
import requests
import telebot
from telebot import types
from dotenv import load_dotenv
from datetime import datetime
import pytz

def convert_utc_to_tz(utc_datetime_str):
    dt = datetime.fromisoformat(utc_datetime_str.replace('Z', '+00:00'))
    ldt = dt.astimezone(TIME_ZONE)
    return ldt.strftime('%Y-%m-%d %H:%M:%S')


load_dotenv()


bot = telebot.TeleBot(os.getenv('TOKEN'))
MY_API_URL = os.getenv('API_URL')
TIME_ZONE = pytz.timezone(os.getenv('TIME_ZONE'))


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    body = {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
    }
    try:
        response = requests.post(f'{MY_API_URL}/register/', json=body)
    except requests.exceptions.ConnectionError:
        bot.send_message(message.chat.id, 'Произошла непредвиденная ошибка,\nпроверьте состояние сервера API')
        return None
    if response.status_code == 201:
        datetime = convert_utc_to_tz(response.json()['registered_at'])
        name = response.json()['username']
        if name == '':
            name = 'без имени'
        else:
            name = 'под именем ' + name
        id = response.json()['user_id']
        bot.send_message(message.chat.id, f'Вы зарегистрированы {datetime} {name}\nВаш id: {id}')
    elif response.status_code == 200:
        bot.send_message(message.chat.id, 'Вы уже были зарегистрированы')
    else:
        bot.send_message(message.chat.id, 'Произошла какая-то ошибка')

@bot.message_handler(commands=['myinfo'])
def my_info(message: types.Message):
    try:
        response = requests.get(f'{MY_API_URL}/userinfo/{message.from_user.id}/')
    except requests.exceptions.ConnectionError:
        bot.send_message(message.chat.id, 'Произошла непредвиденная ошибка,\nпроверьте состояние сервера API')
        return None

    if response.status_code == 200:
        datetime = convert_utc_to_tz(response.json()['registered_at'])
        name = response.json()['username']
        if name == '':
            name = 'без имени'
        else:
            name = 'под именем ' + name
        id = response.json()['user_id']
        bot.reply_to(message, f'Вы были зарегистрированы {datetime}\n{name}')
    else:
        bot.reply_to(message, 'Видимо вы еще не зарегистрированы,\n выполните команду /start для регистрации.')



if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)


