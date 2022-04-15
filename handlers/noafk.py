from pyrogram import Client, filters

from database import tgusers, groupsettings

from utils import timehelper, autoDelete
from utils.formatutils import autobool


@Client.on_message(filters.command(['noafk']) & filters.private & ~filters.edited)
async def noafk(c, m):

    status = tgusers.online_user(m.from_user)


    if status and status.get('afk_status', False):

        elapsed = timehelper.readableTime(timehelper.getDuration(status['seen']))
        
        x = await m.reply("{mention} is no longer AFK{afk_since}\nReason: {reason}".format(
                mention=f'[{m.from_user.first_name}](tg://user?id={m.from_user.id})',
                afk_since=f"\nAFK since: {elapsed}" if not autobool(status.get('privacy_time', False))['bool'] else "",
                reason='`' + status['reason'] + '`' if status['reason'] else "Not specified",
            ), parse_mode = 'markdown')


        if m.chat.type != 'private':
            
            group_settings = groupsettings.find_by_id(m.chat.id)
            
            if group_settings and group_settings.get('cleanup', 'false') != 'false':
                        
                autoDelete.newDeleteJob(chat_id = m.chat.id, message_id = x.message_id, delete_delay = group_settings['cleanup'])