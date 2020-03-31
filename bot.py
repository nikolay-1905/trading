from pandas_datareader import data as wb
from math import *
import telebot
import config
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Напиши токен компании')

@bot.message_handler(content_types=["text"])
def send_text(message):
    try:
        tickers = [message.text.upper()]
        img = wb.DataReader(tickers, 'yahoo', '2017-01-01')
        img = img.reset_index()
        img.columns = ['Date', '1', '2', '3', '4', 'A', 'B']
        img.plot(x='Date', y='3')
        pric = str(wb.get_quote_yahoo(tickers)['price']).split()  # цена
        pric = pric[:-4]
        pric.reverse()
        pric = ' '.join(pric)
        plt.savefig('/Users/nikolaj/PycharmProjects/tradingBot/photo/foo1.png')
        bot.send_photo(message.chat.id, open('/Users/nikolaj/PycharmProjects/tradingBot/photo/foo1.png', 'rb'))
        os.remove("/Users/nikolaj/PycharmProjects/tradingBot/photo/foo1.png")
        bot.send_message(message.chat.id, pric)
    except:
        bot.send_message(message.chat.id, "Ваш токен неправильный")

bot.polling(none_stop=True, interval=0)