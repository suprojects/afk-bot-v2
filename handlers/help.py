from pyrogram import enums, filters
from pyrogram.client import Client


@Client.on_message(filters.command("help") & filters.private)
async def help(_, m):

    await m.reply(
        "Hello {mention}\n\nI'm a simple AFK Bot\nMy primary purpose is to let others know that you are Away-from-Keyboard, so they won't be hanging for your reply\n\nI work the best when added to your group (admin privileges not required!)\n\nSend /commands to learn about my commands".format(
            mention=f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})",
        )
    )


@Client.on_message(filters.command("commands") & filters.private)
async def commands_help(_, m):

    await m.reply(
        """
/afk `[reason]` - Set your AFK status
- You can also add a custom AFK photo/video/gif by attaching a media and adding the command in caption
- You can also reply to a media with the AFK Command
/afk `[reason]`

/noafk - Remove your AFK status (private only)
- __Any message sent in a group AFK status (add #afk tag in your message to preserve your AFK status)__


/seen `[@username/id]` - Check when a user was last seen

/settings - Configure your settings (PM and group)

/start - Show the start message
/help - Show the help message
/commands - Show this message
""",
        parse_mode=enums.ParseMode.MARKDOWN,
    )
