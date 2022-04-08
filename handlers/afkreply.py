from database import tgusers
from pyrogram import Client, filters
from utils import timehelper
from handlers import noafk

@Client.on_message(filters.reply & filters.group & ~filters.regex('^/'))
async def afk_replier(client, message):
    
    await noafk.noafk(client, message)
    
    mentioned = message.reply_to_message.from_user
    status = tgusers.if_afk(mentioned.id)
    
    if status.get('afk_status', False):
        
        reply_message = ("""
{mention} is AFK{afk_since}
Reason: {reason}
            """.format(
                mention=f'[{mentioned.first_name}](tg://user?id={mentioned.id})',
                afk_since=f"\nAFK since: {timehelper.readableTime(timehelper.getDuration(status['seen']))}" if status.get('privacy_time', False) else "",
                reason='`' + status['reason'] + '`' if status['reason'] else "Not specified",
            )
        )
        

        if status.get('afk_media', False):
            
            if status['afk_media']['type'] == 'video': await message.reply_video(video = status['afk_media']['id'], caption = reply_message, parse_mode = 'markdown')
            elif status['afk_media']['type'] == 'photo': await message.reply_photo(photo = status['afk_media']['id'], caption = reply_message, parse_mode = 'markdown')
            else: await message.reply(reply_message, parse_mode = 'markdown')
            
        else: await message.reply(reply_message, parse_mode = 'markdown')