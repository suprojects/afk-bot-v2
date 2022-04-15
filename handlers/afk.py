from pyrogram import Client, filters

from database import tgusers, groupsettings

from utils import autoDelete


@Client.on_message(filters.command('afk') & ~filters.edited)
async def afk(c, m):
    
    reason = None
    afk_media = None
    
    if m.command[1:]: reason = str(" ".join(m.command[1:]))
    
    if m.photo:
        
        afk_media = {'id': m.photo.file_id, 'type': 'photo'}
        
    if m.video:
        
        if m.video.duration <= 30:
            
            afk_media = {'id': m.video.file_id, 'type': 'video'}
            
        else: 
            
            await m.reply('Duration of the video must be lesser than 30 seconds')
            return


    tgusers.afked(m.from_user, reason, afk_media)

    x = await m.reply("{mention} is now AFK\nReason: {reason}".format(
            mention=f'[{m.from_user.first_name}](tg://user?id={m.from_user.id})',
            reason='`' + reason + '`' if reason else "Not specified",
        ), parse_mode = 'markdown')


    if m.chat.type != 'private':
        
        group_settings = groupsettings.find_by_id(m.chat.id)

        if group_settings.get('cleanup', 'false') != 'false':
            
            autoDelete.newDeleteJob(chat_id = m.chat.id, message_id = x.message_id, delete_delay = group_settings['cleanup'], delete_command=group_settings.get('cleanup_commands', False), command_id=x.reply_to_message_id)