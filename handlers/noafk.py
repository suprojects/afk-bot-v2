from pyrogram import Client, filters
from database import tgusers
from utils import timehelper

@Client.on_message(filters.group & ~filters.regex('#afk'))
async def noafk(client, message):

    param = tgusers.online_user(message.from_user)

    if param['afk_status']:
        elapsed = timehelper.readableTime(timehelper.getDuration(param['seen']))
        
        await message.reply("""
{mention} is no longer AFK
AFK since: {elapsed}
Reason: {reason}
""".format(
    mention=f'[{message.from_user.first_name}](tg://user?id={message.from_user.id})',
    elapsed=elapsed,
    reason='`' + param['reason'] + '`' if param['reason'] else "Not specified",
    ), parse_mode = 'markdown')