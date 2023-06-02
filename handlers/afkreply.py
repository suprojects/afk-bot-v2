import re

from pyrogram import enums, filters
from pyrogram.client import Client
from pyrogram.errors import exceptions
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import groupsettings, tgusers
from handlers import noafk
from utils import autoDelete, timehelper
from utils.formatutils import autobool


@Client.on_message(filters.group & ~filters.regex("^/"))
async def afk_replier(c, m):

    if m.text:
        if not re.search("#afk", m.text):
            await noafk.noafk(c, m)

    else:
        await noafk.noafk(c, m)

    if m.reply_to_message and m.reply_to_message.from_user:
        status = tgusers.find_by_id(m.reply_to_message.from_user.id)

    elif m.entities:
        if (len(m.entities) == 1 and m.entities[0].type == enums.MessageEntityType.MENTION):
            entities = m.entities[0]
            status = tgusers.find_by_username(str(m.text)[entities.offset + 1 : entities.length + entities.offset])
        else: return

    else: return


    if status and status.get("afk_status", False):

        try:
            member = await c.get_chat_member(m.chat.id, status["id"])

        except exceptions.bad_request_400.UserNotParticipant:
            return

        else:
            if member.status in [
                enums.ChatMemberStatus.OWNER,
                enums.ChatMemberStatus.ADMINISTRATOR,
                enums.ChatMemberStatus.MEMBER,
            ]:
                reply_message = "{mention} is AFK{afk_since}\nReason: {reason}".format(
                    mention=f"[{status['first_name']}](tg://user?id={status['id']})",
                    afk_since=""
                    if autobool(status.get("privacy_time", False))["bool"]
                    else f"\nAFK since: {timehelper.readableTime(timehelper.getDuration(status['seen']))}",
                    reason="`" + status["reason"] + "`"
                    if status["reason"]
                    else "Not specified",
                )

                group_settings = groupsettings.find_by_id(m.chat.id)

                if (
                    status.get("afk_media", False)
                    and group_settings
                    and group_settings.get("afk_media", True)
                ):
                    if status["afk_media"]["type"] == "video":
                        x = await m.reply_video(
                            video=status["afk_media"]["id"],
                            caption=reply_message,
                            parse_mode=enums.ParseMode.MARKDOWN,
                        )

                    elif status["afk_media"]["type"] == "photo":
                        x = await m.reply_photo(
                            photo=status["afk_media"]["id"],
                            caption=reply_message,
                            parse_mode=enums.ParseMode.MARKDOWN,
                        )

                    else:
                        x = await m.reply(
                            reply_message,
                            parse_mode=enums.ParseMode.MARKDOWN,
                            disable_web_page_preview=True,
                        )

                else:
                    x = await m.reply(
                        reply_message,
                        parse_mode=enums.ParseMode.MARKDOWN,
                        disable_web_page_preview=True,
                    )

                if (status.get("mention_log", False) and status.get("bot_user", False) and not (m.from_user.is_self if m.from_user else False)):

                    await c.send_message(
                        chat_id=status["id"],
                        text="{mention} mentioned you in {title}\nAFK Duration: {elapsed}\n\n__{message}__".format(
                            mention=f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})" if m.from_user else "An admin",
                            title=f"[{m.chat.title}](tg://resolve?domain={m.chat.username})" if m.chat.username else f"{m.chat.title}",
                            elapsed=timehelper.readableTime(timehelper.getDuration(status["seen"])),
                            message=m.text,
                        ),
                        parse_mode=enums.ParseMode.MARKDOWN,
                        protect_content=True,
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton(text="Go to Message", url=m.link)]]
                        ),
                    )

                if group_settings and group_settings.get("cleanup", "false") != "false":
                    autoDelete.newDeleteJob(
                        chat_id=m.chat.id,
                        message_id=x.id,
                        delete_delay=group_settings["cleanup"],
                    )
