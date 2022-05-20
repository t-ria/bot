import telebot  # pyTelegramBotAPI	4.3.1
from telebot import types
import requests
from bs4 import BeautifulSoup as b
#import menu
#from menu import Knopki



bot = telebot.TeleBot('5129343704:AAEQ0O6FhQ_tno-PJzgaLe4cDy0vZHGWa00')


# -----------------------------------------------------------------------
@bot.message_handler(commands=["start"])
def command(message):

    markup = types.InlineKeyboardMarkup()
    k_start = types.InlineKeyboardButton("Начать игру")
    k_help = types.KeyboardButton("Помощь")
    k_exit = types.KeyboardButton("Выход")
    markup.add(k_start, k_help, k_exit)

    bot.send_message(message.chat.id, 'Приветсвую, {0.first_name}! В этом боте ты сможешь сыгать в популярную игра "ГДЕ ЛОГИКА"'.format(message.from_user), reply_markup=markup)
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEEuKFif1KLuqZ2P7byDw7L-awRpL43OAACsRIAAtjY4QABhKwwKld-hAokBA")


# -----------------------------------------------------------------------
@bot.message_handler(content_types= ['text'])
def bot_messege(message):

    if message.text == "Начать":

       


    if message.text == "Помощь":
        send_help(message)

    elif message.text == 'Выход':
        markup = types.InlineKeyboardMarkup()
        k_start = types.InlineKeyboardButton("Начать игру")
        k_help = types.KeyboardButton("Помощь")
        markup.add(k_start, k_help)
        bot.send_message(message.chat.id, 'Выход', reply_markup=markup)




@bot.callback_query_handler(func=lambda call: True)
def send_help(message):
    bot.send_message(message.chat.id, "Автор: Виктория Черепко")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/t_o_ria")
    markup.add(btn1)
    img = open('Черепко Виктория.gpg', 'rb')
    bot.send_photo(message.chat.id, img, reply_markup=markup)

# -----------------------------------------------------------------------
bot.polling(none_stop=True)  # Запускаем бота



