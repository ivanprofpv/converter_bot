import os

import telebot

from dotenv import load_dotenv
from google_currency import convert
from telebot import types
import json

load_dotenv()
key = os.getenv("KEY")

bot = telebot.TeleBot(key)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Введите сумму:')
    bot.register_next_step_handler(message, input_summa)


def input_summa(message):
    try:
        amount = int(message.text.strip())
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('RUB/USD', callback_data=f'RUB/USD/{str(amount)}')
        btn2 = types.InlineKeyboardButton('USD/RUB', callback_data=f'USD/RUB/{amount}')
        btn3 = types.InlineKeyboardButton('RUB/EUR', callback_data=f'RUB/EUR/{amount}')
        btn4 = types.InlineKeyboardButton('EUR/RUB', callback_data=f'EUR/RUB/{amount}')
        btn5 = types.InlineKeyboardButton('CNY/RUB', callback_data=f'CNY/RUB/{amount}')
        btn6 = types.InlineKeyboardButton('RUB/CNY', callback_data=f'RUB/CNY/{amount}')
        btn7 = types.InlineKeyboardButton('EUR/USD', callback_data=f'EUR/USD/{amount}')
        btn8 = types.InlineKeyboardButton('USD/EUR', callback_data=f'USD/EUR/{amount}')
        btn9 = types.InlineKeyboardButton('Другая валюта', callback_data=f'other_currency/{amount}')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
        bot.send_message(message.chat.id, f'Выберите, какую валюту сконвертировать:', reply_markup=markup)
    except ValueError:
        bot.send_message(message.chat.id, f'Ошибка. Необходимо ввести число. Чтобы начать сначала, нажмите /start')
        bot.register_next_step_handler(message, start)
        return


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if 'other_currency' not in call.data:
        values = call.data.strip().split('/') # Создаем список из callback_data для обычной валюты
        total_values = convert(values[0], values[1], int(values[2]))
        data = json.loads(total_values)
        bot.send_message(call.message.chat.id, f'Результат: {data["amount"]} {values[1]}')
        bot.send_message(call.message.chat.id, f'Вы можете выбрать другую валюту или нажмите /start, чтобы ввести новую сумму.')
    else:
        values = call.data.strip().split('/')  # Создаем список из callback_data для своей валюты
        amount_for_my_currency = int(values[1]) # Берем значение {amount} из callback_data для своей валюты
        bot.send_message(call.message.chat.id, f'Введите код валюты в формате: RUB/USD, где RUB - ваша валюта, а USD - во что будем конвертировать:')
        bot.register_next_step_handler(call.message, my_currency, amount_for_my_currency) # передаем значение {amount} в my_currency


def my_currency(message, amount_for_my_currency):
    try:
        values = message.text.split('/')
        total_values = convert(values[0], values[1], amount_for_my_currency)
        data = json.loads(total_values)
        bot.send_message(message.chat.id, f'Результат: {data["amount"]} {values[1]}')
        bot.send_message(message.chat.id, f'Вы можете выбрать другую валюту или нажмите /start, чтобы ввести новую сумму.')
    except IndexError:
        bot.send_message(message.chat.id, f'Введите код валюты в формате: RUB/USD, где RUB - ваша валюта, а USD - во что будем конвертировать:')
        bot.register_next_step_handler(message, my_currency, amount_for_my_currency)
        return


@bot.message_handler()
def start_else_not_command(message):
    bot.send_message(message.chat.id, f'Нажмите /start, чтобы ввести новую сумму.')
    bot.register_next_step_handler(message, input_summa)

bot.infinity_polling()
