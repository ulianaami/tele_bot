import telebot
from settings import TOKEN
from telebot import types
import random

bot = telebot.TeleBot(TOKEN)

file = open('affirmations.txt', 'r', encoding='UTF-8')
affirmations = file.read().split('\n')
file.close()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    username = message.from_user.username
    if message.text == 'Привет' or message.text == 'привет':
        bot.send_message(message.from_user.id, f'Привет, {username}\nНапиши: "Аффирмация"')
        bot.register_next_step_handler(message, give_affirmation)
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'Напиши: "Привет"')
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю. Напиши /help.')


@bot.message_handler(func=lambda m: True)
def give_affirmation(message):
    if message.text == 'аффирмация' or message.text == 'Аффирмация':
        keyboard = types.InlineKeyboardMarkup()
        key_affirmation = types.InlineKeyboardButton(text='Получить позитивную аффирмацию', callback_data='get_affirm')
        keyboard.add(key_affirmation)
        bot.send_message(message.from_user.id, text='Чтобы получить позитивную аффирмацию, нажми на кнопку: ',
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'get_affirm':
        bot.send_message(call.message.chat.id, random.choice(affirmations))


bot.infinity_polling()


