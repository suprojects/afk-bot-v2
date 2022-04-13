from pyrogram import Client, filters

from database import tgusers

from utils import timehelper

from utils.formatutils import autobool

from database import groupsettings

from utils import grouputils


@Client.on_message(filters.command(['noafk']) & filters.private & ~filters.edited)
async def noafk(c, m):

    status = tgusers.online_user(m.from_user)
    

    if status:
        
        if status.get('afk_status', False):
            
            elapsed = timehelper.readableTime(timehelper.getDuration(status['seen']))
            
            x = await m.reply("{mention} is no longer AFK{afk_since}\nReason: {reason}".format(
                    mention=f'[{m.from_user.first_name}](tg://user?id={m.from_user.id})',
                    afk_since=f"\nAFK since: {elapsed}" if not autobool(status.get('privacy_time', False))['bool'] else "",
                    reason='`' + status['reason'] + '`' if status['reason'] else "Not specified",
                ), parse_mode = 'markdown')


            if m.chat.type != 'private':
                group_settings = groupsettings.find_by_id(m.chat.id)

                if group_settings.get('cleanup', 'false') != 'false':
        
                    await grouputils.cleanup(m, x, group_settings, delete_reply = False)
            