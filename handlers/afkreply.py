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
        
        reply_message = """
{mention} is AFK
AFK since: {elapsed}
Reason: {reason}
""".format(
    mention=f'[{mentioned.first_name}](tg://user?id={mentioned.id})',
    elapsed=timehelper.readableTime(timehelper.getDuration(status['seen'])),
    reason='`' + status['reason'] + '`' if status['reason'] else "Not specified",
)

        if status.get('afk_media', False): 
            if status['afk_media']['type'] == 'video': await message.reply_video(video = status['afk_media']['id'], caption = reply_message, parse_mode = 'markdown')
            elif status['afk_media']['type'] == 'photo': await message.reply_photo(photo = status['afk_media']['id'], caption = reply_message, parse_mode = 'markdown')
            else: await message.reply(reply_message, parse_mode = 'markdown')
            
        else: await message.reply(reply_message, parse_mode = 'markdown')