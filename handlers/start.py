from pyrogram import filters
from pyrogram.client import Client

from database import tgusers


@Client.on_message(filters.private & filters.command(["start"]))
async def start_pvt(_, message):
    tgusers.new_botuser(message.from_user)
    await message.reply(
        "Hey there!\n\nI am a simple AFK Bot. I tell users that you are away if you are, so they dont need to be hanging for your reply.\n\nSend /help for usage instructions"
    )
