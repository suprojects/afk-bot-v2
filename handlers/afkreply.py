from database import tgusers, groupsettings

from pyrogram import Client, filters
from pyrogram.types import ChatMember, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import exceptions

from utils import timehelper
from utils.formatutils import autobool

from handlers import noafk

import re

@Client.on_message(filters.group & ~filters.regex('^/'))
async def afk_replier(c, m):

    if m.text:
        if not re.search('#afk', m.text):
            await noafk.noafk(c, m)


    if m.reply_to_message:
        status = tgusers.find_by_id(m.reply_to_message.from_user.id)   

    elif m.entities:
        
        if len(m.entities) == 1 and m.entities[0].type == 'mention':
            
            entities = m.entities[0]
            status = tgusers.find_by_username(str(m.text)[entities.offset + 1 : entities.length + entities.offset])

        else: return
        
    else: return
    

    if status.get('afk_status', False):
         
        try:
            member = await c.get_chat_member(m.chat.id, status['id'])
            
        except exceptions.bad_request_400.UserNotParticipant: 
            return
        
        else:
        
            if member.status == 'creator' or member.status == 'administrator' or member.status == 'member':
                
                reply_message = ("{mention} is AFK{afk_since}\nReason: {reason}".format(
                        mention=f"[{status['first_name']}](tg://user?id={status['id']})",
                        afk_since=f"\nAFK since: {timehelper.readableTime(timehelper.getDuration(status['seen']))}" if not autobool(status.get('privacy_time', False))['bool'] else "",
                        reason='`' + status['reason'] + '`' if status['reason'] else "Not specified",
                    )
                )

                if status.get('afk_media', False) and groupsettings.find_by_id(m.chat.id).get('afk_media', True):
   
                    if status['afk_media']['type'] == 'video': await m.reply_video(video = status['afk_media']['id'], caption = reply_message, parse_mode = 'markdown')
                    elif status['afk_media']['type'] == 'photo': await m.reply_photo(photo = status['afk_media']['id'], caption = reply_message, parse_mode = 'markdown')
                    else: await m.reply(reply_message, parse_mode = 'markdown', disable_web_page_preview = True)
                    
                else:
                    await m.reply(reply_message, parse_mode = 'markdown', disable_web_page_preview = True)

                
                if status.get('mention_log', False) and status.get('bot_user', False):
                    await c.send_message(
                        chat_id = status['id'],
                        text = "{mention} mentioned you in {title}\nAFK Duration: {elapsed}\n\n__{message}__".format(
                            mention = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})",
                            title = f"[{m.chat.title}](tg://resolve?domain={m.chat.username})" if m.chat.username else f"{m.chat.title}",
                            elapsed = timehelper.readableTime(timehelper.getDuration(status['seen'])),
                            message = m.text,
                        ),
                        parse_mode = 'markdown',
                        protect_content = True,
                        disable_web_page_preview = True,
                        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = 'Go to Message', url = m.link)]]),
                    )