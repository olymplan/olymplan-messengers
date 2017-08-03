# -*- coding: utf-8 -*-
import telebot
import pickle
import datetime
import os.path
import requests
import json
from collections import defaultdict
from my_lib import *
from consts import *
from telebot import types

usersfile = 'users.p'

bot = telebot.TeleBot(BOT_TOKEN)
users = {}
if os.path.isfile(usersfile) and os.path.getsize(usersfile) > 0:
    with open(usersfile, 'rb') as f:
        users = pickle.load(f)

def id_saver(func):
    def wrapped(*args, **kwargs):
        global users
        message = args[0]
        if message.from_user.username:
            users[message.from_user.username] = message.chat.id
            with open(usersfile, 'wb') as f:
                pickle.dump(users, f)
        return func(*args, **kwargs)
    return wrapped

print("----------\nSTARTED!\n----------")

@id_saver
@bot.message_handler(commands=['start'])
def handle_start(message):
    """
    Shows keyboard.
    """
    debug_message(message)
    if message.chat.type == "private":
        bot.send_message(message.chat.id, START_MESSAGE_PRIVATE)

@id_saver
@bot.message_handler(commands=['menu'])
def handle_menu(message):
    """
    Shows keyboard.
    """
    debug_message(message)
    if message.chat.type == "private":
        bot.send_message(message.chat.id, MENU_MESSAGE_PRIVATE)

@id_saver
@bot.message_handler(commands=['schedule'])
def handle_menu(message):
    """
    Checks schedule by username
    """
    debug_message(message)
    if message.chat.type == "private":
        try:
            contests = requests.get('http://dev.olymplan.ru/api/schedule/tg/' + message.from_user.username, timeout=2).text
        except requests.exceptions.Timeout as e:
            print('No user {} in api'.format(message.from_user.username))
            bot.send_message(message.chat.id, SCHEDULE_NO_USER.format(message.from_user.username))
            return
        bot.send_message(message.chat.id, contests)

@id_saver
@bot.message_handler(commands=['help'])
def handle_help(message):
    """
    Shows help.
    """
    debug_message(message)
    msg = bot.send_message(message.chat.id, HELP_MESSAGE)

@bot.message_handler(commands=['commands'])
@id_saver
def handle_commands(message):
    """
    Shows commands.
    """
    debug_message(message)
    bot.send_message(message.chat.id, COMMANDS)

@id_saver
@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    """
    Cancels current action:
    removes user's id from user_actions dictionary if it is there.
    Shows menu after cancelation.
    """
    debug_message(message)

@id_saver
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
