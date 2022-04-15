from pyrogram import Client, filters


@Client.on_message(filters.command("help") & filters.private & ~filters.edited)
async def help(c,m):

    await m.reply("Hello {mention}\n\nI'm a simple AFK Bot\nMy primary purpose is to let others know that you are Away-from-Keyboard, so they won't be hanging for your reply\n\nI work the best when added to your group (admin privileges not required!)\n\nSend /commands to learn about my commands".format(
        mention = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})",
        )
    )
    
@Client.on_message(filters.command('commands') & filters.private & ~filters.edited)
async def commands_help(c,m):

    await m.reply("""
/afk `[reason]` - Set your AFK status
- You can also add a custom AFK media by adding a caption
/afk `[reason]`

/noafk - Remove your AFK status (private only)
- __Any message sent in a group AFK status (add #afk tag in your message to preserve your AFK status)__


/seen `[@username/id]` - Check when a user was last seen

/settings - Configure your settings (PM and group)

/start - Show the start message
/help - Show the help message
/commands - Show this message
""", parse_mode = 'markdown')