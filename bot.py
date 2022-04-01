from pyrogram import Client

import configparser
config = configparser.ConfigParser()
config.read('config.ini')
bot = config['tokens']

print('initiated')

Client("bot", bot_token = str(bot['api_token'])).run()
