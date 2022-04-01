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
    mention=f'[{mentioned.first_name}](tg://user?id={mentioned.id})',
    reason='`' + status['reason'] + '`' if status['reason'] else "Not specified",
), parse_mode = 'markdowm')