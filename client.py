from pyrogram import Client


import configparser
config = configparser.ConfigParser()
config.read('config.ini')
bot = config['tokens']


client = Client("bot", bot_token = str(bot['api_token']))