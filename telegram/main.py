# -*- coding: utf-8 -*-
import telebot
import pickle
import datetime
import re
from collections import defaultdict
from my_lib import *
from consts import *
from telebot import types


bot = telebot.TeleBot(BOT_TOKEN)

user_actions = {}

print("----------\nSTARTED!\n----------")

@bot.message_handler(commands=['start'])
def handle_start(message):
    """
    Shows keyboard.
    """
    debug_message(message)
    if message.chat.type == "private":
        bot.send_message(message.chat.id, START_MESSAGE_PRIVATE)

@bot.message_handler(commands=['menu'])
def handle_menu(message):
    """
    Shows keyboard.
    """
    debug_message(message)
    if message.chat.type == "private":
        bot.send_message(message.chat.id, MENU_MESSAGE_PRIVATE)

@bot.message_handler(commands=['help'])
def handle_help(message):
    """
    Shows help.
    """
    debug_message(message)
    msg = bot.send_message(message.chat.id, HELP_MESSAGE)

@bot.message_handler(commands=['commands'])
def handle_commands(message):
    """
    Shows commands.
    """
    debug_message(message)
    bot.send_message(message.chat.id, COMMANDS)

@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    """
    Cancels current action:
    removes user's id from user_actions dictionary if it is there.
    Shows menu after cancelation.
    """
    debug_message(message)

@bot.message_handler(content_types=['text'])
def handle_message(message):
    """
    Handles three different menu commands:
    "Check schedule", "Check hometask" and "Add hometask".
    """
    bot.send_message(message.chat.id, 'Привет, это Олимплан!')

def debug_message(message):
    """
    Prints information about message to console.
    """
    print('[{}]\n>> "{}"\n>> From "{} {}" (@{} : {}) in chat "{}" ({}). Message id: {}'.format(
        datetime.datetime.fromtimestamp(message.date).strftime('%d.%m.%Y %H:%M:%S'),
        message.text,
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.username,
        message.from_user.id,
        message.chat.title,
        message.chat.id,
        message.message_id))

bot.polling()
