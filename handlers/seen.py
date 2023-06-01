from pyrogram import enums, filters
from pyrogram.client import Client

from utils import timehelper, userFinder
from utils.formatutils import autobool


@Client.on_message(filters.private & filters.command(["seen"]) & ~filters.edited)
async def seenViewer(_, m):

    if param := m.command[1:]:
        if mentioned := userFinder.find(param[0]):
            if mentioned.get("seen", False):

                if mentioned.get("afk_status", False):

                    reply_message = "{mention} is AFK{afk_since}\nReason: {reason}".format(
                        mention=f"[{mentioned['first_name']}](tg://user?id={mentioned['id']})",
                        afk_since=f"\nAFK since: {timehelper.readableTime(timehelper.getDuration(mentioned['seen']))}"
                        if autobool(not mentioned.get("privacy_time", False))["bool"]
                        else "",
                        reason="`" + mentioned["reason"] + "`"
                        if mentioned["reason"]
                        else "Not specified",
                    )

                    if mentioned.get("afk_media", False):

                        if mentioned["afk_media"]["type"] == "video":
                            await m.reply_video(
                                video=mentioned["afk_media"]["id"],
                                caption=reply_message,
                                parse_mode=enums.ParseMode.MARKDOWN,
                            )

                        elif mentioned["afk_media"]["type"] == "photo":
                            await m.reply_photo(
                                photo=mentioned["afk_media"]["id"],
                                caption=reply_message,
                                parse_mode=enums.ParseMode.MARKDOWN,
                            )

                        else:
                            await m.reply(
                                reply_message, parse_mode=enums.ParseMode.MARKDOWN
                            )

                    else:
                        await m.reply(
                            reply_message, parse_mode=enums.ParseMode.MARKDOWN
                        )

                elif not mentioned.get("privacy_seen", False):

                    await m.reply(
                        "Last seen {mention} before {elapsed}".format(
                            mention=f"[{mentioned['first_name']}](tg://user?id={mentioned['id']})",
                            elapsed=timehelper.readableTime(
                                timehelper.getDuration(mentioned["seen"])
                            ),
                        )
                    )

                else:
                    await m.reply(
                        "`{mentioned}` not seen before".format(mentioned=param[0]),
                        parse_mode=enums.ParseMode.MARKDOWN,
                    )

            else:
                await m.reply(
                    "`{mentioned}` not seen before".format(mentioned=param[0]),
                    parse_mode=enums.ParseMode.MARKDOWN,
                )

        else:
            await m.reply(
                "`{mentioned}` not seen before".format(mentioned=param[0]),
                parse_mode=enums.ParseMode.MARKDOWN,
            )

    else:
        await m.reply("Use format `/seen id` or `/seen @username`")
