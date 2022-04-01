from pyrogram import Client, filters
from database import tgusers
from utils import timehelper

@Client.on_message(filters.group & ~filters.regex('#afk') & filters.text)
async def noafk(client, message):
    
    param = tgusers.online_user(message.from_user)

    if param['afk_status']:
        
        elapsed = timehelper.readableTime(timehelper.getDuration(param['seen']))
        
        await message.reply(f"""
[{message.from_user.first_name}](tg://user?id={message.from_user.id}) is no longer AFK
AFK since: {elapsed}
Reason: {'`' + param['reason'] + '`' if param['reason'] else "Not specified"}
""", parse_mode = 'markdown')