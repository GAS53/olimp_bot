from datetime import datetime

import telebot
from telebot import types
from telebot.handler_backends import State, StatesGroup
from telebot import custom_filters


import settings
import preparater


bot = telebot.TeleBot(settings.TOKEN)

di = preparater.prepate()

class MyStates(StatesGroup):
    get_key = State()


@bot.message_handler(commands=['start'])
def main_run(message: types.Message):
    bot.send_message(message.from_user.id, '''Этот бот для прохождения теста 1793.3
    \n необходимо ввести самое редко встречающееся слово из вопроса''')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    find = types.KeyboardButton(text='Найти')
    markup.row(find)
    bot.send_message(message.from_user.id, 'Что ищем?', reply_markup=markup)
    






@bot.message_handler(state=MyStates.get_key)
def get_key(message):
    with bot.retrieve_data(message.from_user.id, message.from_user.id) as data:
        data['get_key'] = message.text

    res = preparater.finder(di, data['get_key'])
    if res:
        bot.send_message(message.from_user.id, f"{data['get_key']}\n{res}")
        with open(settings.LOG, 'a') as file:
            file.write(f"{datetime.now()} {message.from_user.id} {data['get_key']}\n  ")
    else:
        bot.send_message(message.from_user.id, f"вопрос с таким значением не найден {data['get_key']}")

    bot.send_message(message.from_user.id, 'Заново /start')

def get_state(message):
    bot.set_state(message.from_user.id, MyStates.get_key, message.from_user.id)
    bot.send_message(message.from_user.id, 'введите что ищем')




@bot.message_handler(content_types=['text'])
def send_text(message: types.Message):
    if message.text.lower() == 'найти':
        get_state(message)
    else:
        bot.send_message(message.from_user.id, f"неверная команда- '{message.text}'")




if __name__ == '__main__':
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.polling(interval=settings.BOT_CHECK_INTERVAL, none_stop=True)