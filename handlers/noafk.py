from pyrogram import enums, filters
from pyrogram.client import Client

from database import groupsettings, tgusers
from utils import autoDelete, timehelper
from utils.formatutils import autobool


@Client.on_message(filters.command(["noafk"]) & filters.private)
async def noafk(_, m):
    status = tgusers.online_user(m.from_user)

    if status and status.get("afk_status", False):
        elapsed = timehelper.readableTime(timehelper.getDuration(status["seen"]))

        x = await m.reply(
            "{mention} is no longer AFK{afk_since}\nReason: {reason}".format(
                mention=f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})",
                afk_since=""
                if autobool(status.get("privacy_time", False))["bool"]
                else f"\nAFK since: {elapsed}",
                reason="`" + status["reason"] + "`"
                if status["reason"]
                else "Not specified",
            ),
            parse_mode=enums.ParseMode.MARKDOWN,
        )

        if m.chat.type != "private":
            group_settings = groupsettings.find_by_id(m.chat.id)

            if group_settings and group_settings.get("cleanup", "false") != "false":
                autoDelete.newDeleteJob(
                    chat_id=m.chat.id,
                    id=x.id,
                    delete_delay=group_settings["cleanup"],
                )
