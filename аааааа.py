import telebot  # pyTelegramBotAPI	4.3.1
from telebot import types
import requests
import bs4
import botGames
import class_menu
from class_menu import Menu, Users
bot = telebot.TeleBot('5129343704:AAEQ0O6FhQ_tno-PJzgaLe4cDy0vZHGWa00')


# -----------------------------------------------------------------------
@bot.message_handler(commands=["start"])
def command(message, res=False):
    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Главное меню")
    btn2 = types.KeyboardButton("❓ Помощь(мне нужна)")
    markup.add(btn1, btn2)

    bot.send_message(chat_id,
                     text="Привет, {0.first_name}! Я недоделанный бот, и я ничего не умею".format(
                         message.from_user), reply_markup=markup)
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEEQXRiPK2HXCCsXExpgoeJf4ReHXhQOwAC6B8AAtjY4QABDYxCQyBiSoYjBA")

# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text
    cur_user = Users.getUser(chat_id)
    if cur_user == None:
        cur_user = Users(chat_id, message.json["from"])
        subMenu = class_menu.goto_menu(bot, chat_id, ms_text)




    if ms_text == "Помощь":
       # send_help(chat_id)
        pass


    elif ms_text == "Прислать кошку":
        bot.send_photo(chat_id, photo=get_catURL(), caption="Лови котика!!")


    elif ms_text == "Прислать анекдот":
        bot.send_message(chat_id, text=get_anekdot())

    elif ms_text == "Прислать новости":
        bot.send_message(chat_id, text=get_news())

    else:
        bot.send_message(chat_id, text="Мне жаль, я не такой умный, чтобы ответить на: " + ms_text)



@bot.message_handler(content_types=['sticker'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    sticker = message.sticker
    bot.send_message(message.chat.id, sticker)

def goto_menu(chat_id, name_menu):
    # получение нужного элемента меню
    cur_menu = Menu.getcur(chat_id)
    if name_menu == "Выход" and cur_menu != None and cur_menu.parent != None:
        target_menu = Menu.getMenu(chat_id, cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(chat_id, name_menu)

    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)

        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if target_menu.name == "Игра в 21":
            game21 = botGames.newGame(chat_id, botGames.Game21(jokers_enabled=True))  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        elif target_menu.name == "Камень, ножницы, бумага":
            gameRSP = botGames.newGame(chat_id, botGames.GameRPS())  # создаём новый экземпляр игры
            text_game = "<b>Победитель определяется по следующим правилам:</b>\n" \
                        "1. Камень побеждает ножницы\n" \
                        "2. Бумага побеждает камень\n" \
                        "3. Ножницы побеждают бумагу"
            bot.send_photo(chat_id, photo="https://i.ytimg.com/vi/Gvks8_WLiw0/maxresdefault.jpg", caption=text_game, parse_mode='HTML')

        return True
    else:
        return False

#------------------------------------------------------------------------





# -----------------------------------------------------------------------
def getMediaCards(game21):
    medias = []
    for url in game21.arr_cards_URL:
        medias.append(types.InputMediaPhoto(url))
    return medias
    # ----------------------------------------------------------------------


def get_anekdot():
    array_anekdots = []
    req_anek = requests.get('http://anekdotme.ru/random')
    soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
    result_find = soup.select('.anekdot_text')
    for result in result_find:
        array_anekdots.append(result.getText().strip())
    return array_anekdots[0]

# -----------------------------------------------------------------------
def get_catURL():
    url = ""
    req = requests.get('https://genrandom.com/ru/cats/')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['url']
        # url.split("/")[-1]
    return url

# -----------------------------------------------------------------------
bot.polling(none_stop=True, interval=0)  # Запускаем бота

print()
