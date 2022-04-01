from pyrogram import Client, filters
from database import tgusers

@Client.on_message(filters.command('afk') & ~filters.regex('#afk'))
async def afk(client, message):
    
    reason = None
    
    if message.command[1:]:
        reason = str(" ".join(message.command[1:]))
    
    tgusers.afked(message.from_user, reason)
    
    await message.reply("""
{mention} is now AFK
Reason: {reason}
""".format(
    mention=f'[{message.from_user.first_name}](tg://user?id={message.from_user.id})',
    reason='`' + reason + '`' if reason else "Not specified",
), parse_mode = 'markdown')