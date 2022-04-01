from database import tgusers
from pyrogram import Client, filters
from utils import timehelper
from handlers import noafk

@Client.on_message(filters.reply & filters.group & filters.text)
async def afk_replier(client, message):
    
    await noafk.noafk(client, message)
    
    mentioned = message.reply_to_message.from_user
    status = tgusers.if_afk(mentioned.id)
    
    if status['afk_status']:
        await message.reply("""
{mention} is AFK
AFK since: {elapsed}
Reason: {reason}
""".format(
    mention=f'[{mentioned.first_name}](tg://user?id={mentioned.id})',
    elapsed=timehelper.readableTime(timehelper.getDuration(status['seen'])),
    reason='`' + status['reason'] + '`' if status['reason'] else "Not specified",
), parse_mode = 'markdown')
    
 #   await message.reply(status)
#    await message.reply(message)