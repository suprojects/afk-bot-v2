from pyrogram import Client, filters
from database import tgusers
from utils import timehelper, grouputils

@Client.on_message(filters.group & ~filters.regex('#afk') & ~filters.regex('^/') & filters.text)
async def noafk(client, message):

    status = tgusers.online_user(message.from_user)

    if status.get('afk_status', False):
        elapsed = timehelper.readableTime(timehelper.getDuration(status['seen']))
        
        msg = await message.reply("""
{mention} is no longer AFK{afk_since}
Reason: {reason}
""".format(
    mention=f'[{message.from_user.first_name}](tg://user?id={message.from_user.id})',
    afk_since=f"\nAFK since: {elapsed}" if status.get('privacy_time', False) else "",
    reason='`' + status['reason'] + '`' if status['reason'] else "Not specified",
    ), parse_mode = 'markdown')
        
    #await grouputils.cleanup(message = msg)