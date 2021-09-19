import time
import telebot
from helper import Helper
from threading import Thread
from SECRET import telegram_bot_token
from subscribe_json import SubscribeJson
from steam_sales_observer import SteamSalesObserver

bot = telebot.TeleBot(telegram_bot_token)
observer = SteamSalesObserver()
subscribers = SubscribeJson()


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                     Helper.welcome_text.format(name=message.from_user.first_name, me=bot.get_me().first_name),
                     parse_mode='html')


@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    subscribers.subscribe(message.chat.id, message.from_user.first_name)
    bot.send_message(message.chat.id, Helper.subscribe_text)


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    subscribers.unsubscribe(message.chat.id)
    bot.send_message(message.chat.id, Helper.unsubscribe_text)


def beautify_sales(sales):
    result_str = ""
    for sale in sales:
        result_str += f'{sale[0]}\n{sale[1]}\n\n'
    return result_str


def observe_sales(callback):
    while True:
        sales = observer.get_new_sales()
        if len(sales) == 0:
            continue
        for chat_id, name in subscribers.items():
            if callable(callback):
                callback(chat_id, name, beautify_sales(sales))
        time.sleep(24 * 60 * 60)


def sale_callback(chat_id, name, games):
    bot.send_message(chat_id, Helper.new_sales_text.format(name=name, games=games))


def main():
    Thread(target=observe_sales, args=(sale_callback,), daemon=True).start()
