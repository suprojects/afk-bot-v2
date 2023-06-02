from pyrogram import enums, filters
from pyrogram.client import Client

from database import groupsettings, tgusers
from utils import autoDelete


@Client.on_message(filters.command("afk"))
async def afk(c, m):

#fix anon admins sending messages tha trigger the bot
    if m.sender_chat:
        return

    afk_media = None

    reason = " ".join(m.command[1:]) if m.command[1:] else None
    if m.photo:
        afk_media = {"id": m.photo.file_id, "type": "photo"}

    if m.video:
        if m.video.duration <= 30:
            afk_media = {"id": m.video.file_id, "type": "video"}

        else:
            await m.reply("Duration of the video must be lesser than 30 seconds")
            return

    tgusers.afked(m.from_user, reason, afk_media)

    x = await m.reply(
        "{mention} is now AFK\nReason: {reason}".format(
            mention=f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})",
            reason=f"`{reason}`" if reason else "Not specified",
        ),
        parse_mode=enums.ParseMode.MARKDOWN,
    )

    if m.chat.type != "private":
        group_settings = groupsettings.find_by_id(m.chat.id)

        if group_settings and group_settings.get("cleanup", "false") != "false":
            autoDelete.newDeleteJob(
                chat_id=m.chat.id,
                message_id=x.id,
                delete_delay=group_settings["cleanup"],
                delete_command=group_settings.get("cleanup_commands", False),
                command_id=x.reply_to_message_id,
            )
