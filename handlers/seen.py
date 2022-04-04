from pyrogram import Client, filters

from database import tgusers
from utils import timehelper
from utils import userFinder

@Client.on_message(filters.private & filters.command(['seen']))
async def seenViewer(client, m):
    
    param = m.command[1:]
    
    if param:
        mentioned = userFinder.find(param[0])
        if mentioned:
            if mentioned.get('afk_status', False):
                reply_message = """
{mention} is AFK
AFK since: {elapsed}
Reason: {reason}
""".format(
    mention=f"[{mentioned['first_name']}](tg://user?id={mentioned['id']})",
    elapsed=timehelper.readableTime(timehelper.getDuration(mentioned['seen'])),
    reason='`' + mentioned['reason'] + '`' if mentioned['reason'] else "Not specified",
)

                if mentioned.get('afk_media', False): 
                    if mentioned['afk_media']['type'] == 'video': await m.reply_video(video = mentioned['afk_media']['id'], caption = reply_message, parse_mode = 'markdown')
                    elif mentioned['afk_media']['type'] == 'photo': await m.reply_photo(photo = mentioned['afk_media']['id'], caption = reply_message, parse_mode = 'markdown')
                    else: await m.reply(reply_message, parse_mode = 'markdown')
                else: await m.reply(reply_message, parse_mode = 'markdown')
        
            elif not mentioned.get('seen_privacy', False):
                await m.reply("""
Last seen {mention} before {elapsed}      
""".format(
        mention=f"[{mentioned['first_name']}](tg://user?id={mentioned['id']})",
        elapsed=timehelper.readableTime(timehelper.getDuration(mentioned['seen'])),
    ))
                
            else: await m.reply('`{mentioned}` not seen before'.format(mentioned = param[0]), parse_mode = 'markdown')
            
        else: await m.reply('`{mentioned}` not seen before'.format(mentioned = param[0]), parse_mode = 'markdown')
    
    
    else: await m.reply('Use format `/seen id` or `/seen @username`')