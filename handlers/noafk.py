from pyrogram import Client, filters
from database import tgusers
from utils import timehelper, grouputils
from utils.formatutils import autobool


@Client.on_message(filters.command(['noafk']) & filters.private)
async def noafk(c, m):

    status = tgusers.online_user(m.from_user)
    

    if status:
        if status.get('afk_status', False):
            elapsed = timehelper.readableTime(timehelper.getDuration(status['seen']))
            
            msg = await m.reply("{mention} is no longer AFK{afk_since}\nReason: {reason}".format(
                    mention=f'[{m.from_user.first_name}](tg://user?id={m.from_user.id})',
                    afk_since=f"\nAFK since: {elapsed}" if not autobool(status.get('privacy_time', False))['bool'] else "",
                    reason='`' + status['reason'] + '`' if status['reason'] else "Not specified",
                ), parse_mode = 'markdown')
        
    #await grouputils.cleanup(m = msg)