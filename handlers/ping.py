from pyrogram import Client, filters
from datetime import datetime

import configparser
config = configparser.ConfigParser()
config.read('config.ini')
sudo = config['sudo']

@Client.on_message(filters.user(sudo['users'].split(',')) & filters.command('ping'))
async def ping(c, m):
    start_time = datetime.now()
    msg = await m.reply_text("Pinging...")
    end_time = datetime.now()
    ping_time = round((end_time - start_time).total_seconds() * 1000)
    await msg.edit(f"Response Time: {ping_time} ms")