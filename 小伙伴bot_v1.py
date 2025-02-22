# -*- coding: utf-8 -*-

import telebot


API_TOKEN = "7418093343:AAHtR8qcmeEqknS0AeBYxmXv92CLsj6l4hw"
bot = telebot.TeleBot(API_TOKEN)



user_state = {}










@bot.message_handler()
def handle_start_command(message):
    bot.send_message(message.chat.id, "欢迎使用该机器人，机器人正在开发中请耐心等待。。。")



bot.polling(non_stop=True, interval=0)
