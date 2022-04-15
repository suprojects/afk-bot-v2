from pyrogram import Client, filters
from database import tgusers
    
@Client.on_message(filters.private & filters.command(["start"]))
async def start_pvt(client, message):
    tgusers.new_botuser(message.from_user)
    await message.reply("Hey there!\n\nI am a simple AFK Bot. I tell users that you are away if you are, so they dont need to be hanging for your reply.")