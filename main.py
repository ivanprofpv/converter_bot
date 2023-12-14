import os

import telebot

from dotenv import load_dotenv
from google_currency import convert
from telebot import types
import json

load_dotenv()
key = os.getenv("KEY")

bot = telebot.TeleBot(key)

amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Введите сумму:')
    bot.register_next_step_handler(message, input_summa)


def input_summa(message):
    global amount
    try:
        amount = int(message.text.strip())
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('RUB/USD', callback_data='RUB/USD')
        btn2 = types.InlineKeyboardButton('USD/RUB', callback_data='USD/RUB')
        btn3 = types.InlineKeyboardButton('RUB/EUR', callback_data='RUB/EUR')
        btn4 = types.InlineKeyboardButton('EUR/RUB', callback_data='EUR/RUB')
        btn5 = types.InlineKeyboardButton('CNY/RUB', callback_data='CNY/RUB')
        btn6 = types.InlineKeyboardButton('RUB/CNY', callback_data='RUB/CNY')
        btn7 = types.InlineKeyboardButton('EUR/USD', callback_data='EUR/USD')
        btn8 = types.InlineKeyboardButton('USD/EUR', callback_data='USD/EUR')
        btn9 = types.InlineKeyboardButton('Другая валюта', callback_data='other_currency')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
        bot.send_message(message.chat.id, f'Выберите, какую валюту сконвертировать:', reply_markup=markup)
    except ValueError:
        bot.send_message(message.chat.id, f'Ошибка. Введите число!')
        bot.register_next_step_handler(message, start)
        return


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'other_currency':
        values = call.data.split('/')
        total_values = convert(values[0], values[1], amount)
        data = json.loads(total_values)
        bot.send_message(call.message.chat.id, f'Результат: {data["amount"]} {values[1]}')
        bot.send_message(call.message.chat.id, f'Вы можете выбрать другую валюту или нажмите /start, чтобы ввести новую сумму.')
    else:
        bot.send_message(call.message.chat.id, f'Введите код валюты в формате: RUB/USD, где RUB - ваша валюта, а USD - во что будем конвертировать:')
        bot.register_next_step_handler(call.message, my_currency)


def my_currency(message):
    values = message.text.split('/')
    total_values = convert(values[0], values[1], amount)
    data = json.loads(total_values)
    bot.send_message(message.chat.id, f'Результат: {data["amount"]} {values[1]}')
    bot.send_message(message.chat.id, f'Вы можете выбрать другую валюту или нажмите /start, чтобы ввести новую сумму.')


bot.infinity_polling()
