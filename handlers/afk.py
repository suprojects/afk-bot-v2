from pyrogram import Client, filters
from database import tgusers

@Client.on_message(filters.command('afk'))
async def afk(client, message):
    
    reason = None
    afk_media = None
    
    if message.command[1:]: reason = str(" ".join(message.command[1:]))
    
    if message.photo: afk_media = {'id': message.photo.file_id, 'type': 'photo'}
    if message.video:
        if message.video.duration <= 30: afk_media = {'id': message.video.file_id, 'type': 'video'}
        else: 
            await message.reply('Duration of the video must be lesser than 30 seconds')
            return
            
    tgusers.afked(message.from_user, reason, afk_media)

    await message.reply("""
{mention} is now AFK
Reason: {reason}
""".format(
    mention=f'[{message.from_user.first_name}](tg://user?id={message.from_user.id})',
    reason='`' + reason + '`' if reason else "Not specified",
), parse_mode = 'markdown')