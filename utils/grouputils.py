import asyncio
from pyrogram.errors import exceptions

from database import groupsettings

async def cleanup(m, x, settings, delete_reply = False):
    

    if settings.get('cleanup', 'false') != 'false':
        
        await asyncio.sleep(int(settings['cleanup']))
        
        await x.delete()
        
        
        if delete_reply == True and settings.get('cleanup_commands', False):
                                                 
            try:
                
                await x.reply_to_message.delete()
                
            except exceptions.forbidden_403.MessageDeleteForbidden:
                
                groupsettings.setting(m.chat, 'cleanup_commands', False)