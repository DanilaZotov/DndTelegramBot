import telebot
from telebot import types
import random
import gspread

token = 0
bot = telebot.TeleBot(token)
service_account = gspread.service_account(filename="service_account.json")
spread_sheet = service_account.open("botTable")
magicWks = spread_sheet.worksheet("magicItems")
commonWks = spread_sheet.worksheet("commonItems")


Current_empty_row_magic = 0
Current_empty_row_common = 0


def items_count(list_name):
    num_of_items = 1
    num_of_rows = list_name.row_count
    for i in range(2, num_of_rows):
        if len(list_name.row_values(i)):
            num_of_items += 1
        else:
            break
    global Current_empty_row_magic
    Current_empty_row_magic = num_of_items + 1
    return num_of_items


def get_random_magic():
    num_of_items = items_count(magicWks)
    randomvalue = random.randint(2, num_of_items)
    item_values = magicWks.row_values(randomvalue)
    item = "Name: " + item_values[0] + "\nRarety: " + \
           item_values[1] + "\nType: " + item_values[2] + "\nDescription: " + item_values[3]
    return item


def get_random_common():
    num_of_items = items_count(commonWks)
    randomvalue = random.randint(2, num_of_items)
    item_values = commonWks.row_values(randomvalue)
    item = "Name: " + item_values[0] + "\nCost: " + \
           item_values[1] + "\nDamage: " + item_values[2] + "\nAttributes: " + item_values[3]
    return item


# ADD MAGIC ITEM


def read_magic_item(message):
    items_count(magicWks)
    sent = bot.send_message(message.chat.id, 'Введите название предмета')
    bot.register_next_step_handler(sent, process_magic_item_name)


def process_magic_item_name(message):
    magicWks.update_cell(Current_empty_row_magic, 1, message.text)
    sent = bot.send_message(message.chat.id, 'Введите тип предмета')
    bot.register_next_step_handler(sent, process_read_magic_type)


def process_read_magic_type(message):
    magicWks.update_cell(Current_empty_row_magic, 2, message.text)
    sent = bot.send_message(message.chat.id, 'Введите редкость предмета')
    bot.register_next_step_handler(sent, process_read_magic_rarety)


def process_read_magic_rarety(message):
    magicWks.update_cell(Current_empty_row_magic, 3, message.text)
    sent = bot.send_message(message.chat.id, 'Введите описание предмета')
    bot.register_next_step_handler(sent, process_read_magic_description)


def process_read_magic_description(message):
    magicWks.update_cell(Current_empty_row_magic, 4, message.text)
    bot.send_message(message.chat.id, 'Предмет добавлен')

# ADD COMMON ITEM


# def read_common_item(message):
#     common_items_count(commonWks)
#     sent = bot.send_message(message.chat.id, 'Введите название предмета')
#     bot.register_next_step_handler(sent, process_common_item_name)
#
#
# def process_common_item_name(message):
#     commonWks.update_cell(Current_empty_row_magic, 1, message.text)
#     sent = bot.send_message(message.chat.id, 'Введите тип предмета')
#     bot.register_next_step_handler(sent, process_read_common_type)
#
#
# def process_read_common_type(message):
#     commonWks.update_cell(Current_empty_row_magic, 2, message.text)
#     sent = bot.send_message(message.chat.id, 'Введите редкость предмета')
#     bot.register_next_step_handler(sent, process_read_common_rarety)
#
#
# def process_read_common_rarety(message):
#     commonWks.update_cell(Current_empty_row_magic, 3, message.text)
#     sent = bot.send_message(message.chat.id, 'Введите описание предмета')
#     bot.register_next_step_handler(sent, process_read_common_description)
#
#
# def process_read_common_description(message):
#     commonWks.update_cell(Current_empty_row_magic, 4, message.text)
#     bot.send_message(message.chat.id, 'Предмет добавлен')

# MAIN


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Веб-ресурсы')
    item2 = types.KeyboardButton('Магический айтем')
    item3 = types.KeyboardButton('Обычный айтем')
    item4 = types.KeyboardButton('Добавить magic айтем')
    # item5 = types.KeyboardButton('Добавить common айтем')
    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, 'Выберете действие', reply_markup=markup)


# MENU


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Веб-ресурсы':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('dnd.su')
            item2 = types.KeyboardButton('donjon')
            item3 = types.KeyboardButton('generate name')
            back = types.KeyboardButton('Назад')
            markup.add(item1, item2, item3, back)

            bot.send_message(message.chat.id, 'Веб-ресурсы', reply_markup=markup)
        elif message.text == 'dnd.su':
            bot.send_message(message.chat.id, "https://dnd.su/")
        elif message.text == 'donjon':
            bot.send_message(message.chat.id, "https://donjon.bin.sh/5e/")
        elif message.text == 'generate name':
            bot.send_message(message.chat.id, "https://www.fantasynamegenerators.com/")
        elif message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Веб-ресурсы')
            item2 = types.KeyboardButton('Магический айтем')
            item3 = types.KeyboardButton('Обычный айтем')
            item4 = types.KeyboardButton('Добавить magic айтем')
            # item5 = types.KeyboardButton('Добавить common айтем')

            markup.add(item1, item2, item3, item4)

            bot.send_message(message.chat.id, 'Выберете действие', reply_markup=markup)
        elif message.text == 'Магический айтем':
            magic_item = get_random_magic()
            bot.send_message(message.chat.id, f"{magic_item}")
        elif message.text == 'Обычный айтем':
            common_item = get_random_common()
            bot.send_message(message.chat.id, f"{common_item}")
        elif message.text == 'Добавить magic айтем':
            read_magic_item(message)
        # elif message.text == 'Добавить common айтем':
        #     read_common_item(message)


bot.infinity_polling()

