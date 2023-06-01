from datetime import datetime, timedelta, timezone

from pyrogram import enums, filters
from pyrogram.client import Client
from pyrogram.errors import exceptions
from pyrogram.types import InlineKeyboardMarkup

from database import groupsettings
from utils import settingshelper, timehelper
from utils.formatutils import autobool

settings_text = """
Current settings for {chat}:

Chat Cleanup: **{cleanup}**
Delete commands: **{cleanup_commands}**
AFK Media: **{afk_media}**

Language: **{lang}**

__Click the buttons to learn about the settings__

"""


cleanup_text = """
Current settings for {chat}:

Chat Cleanup: **{cleanup}**
Delete commands: **{cleanup_commands}**

__Automatically delete messages sent by bot in a specific period of time__

"""


@Client.on_message(filters.command("start") & filters.group)
async def group_start(_, m):
    groupsettings.new_chat(m.chat)


@Client.on_message(filters.command("settings") & filters.group)
async def settings_group(c, m):

    if m.from_user.id in await get_admins(c, m.chat.id, cache_time=2):

        settings = groupsettings.find_by_id(m.chat.id)

        if settings:

            buttons = settingshelper.btn_maker(group_settings_buttons(settings))

        else:

            await m.reply(
                "Please register the group by using /start@{bot_username} command".format(
                    bot_username=(await c.get_me()).username
                )
            )
            return

        await m.reply(
            text=settings_text.format(
                chat=m.chat.title,
                cleanup=timehelper.readableTime(
                    timehelper.seconds_to_time(settings["cleanup"])
                )
                if settings.get("cleanup", "false") != "false"
                else "Disabled",
                cleanup_commands=(
                    "Enabled"
                    if autobool(settings.get("cleanup_commands", False))["bool"]
                    else "Disabled"
                ),
                afk_media=(
                    "Enabled"
                    if autobool(settings.get("afk_media", True))["bool"]
                    else "Disabled"
                ),
                lang=settings.get("lang", "en"),
            ),
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@Client.on_callback_query(filters.regex("^cleanup"))
async def cleanup(c, m):

    param = m.data.split("_")[1:]

    if param[0] == "help":

        await m.answer(
            "Automatically delete messages sent by the bot in a set interval of time",
            show_alert=True,
        )

    elif param[0] == "configure":

        if m.from_user.id in await get_admins(c, m.message.chat.id):

            settings = groupsettings.find_by_id(m.message.chat.id)
            buttons = settingshelper.btn_maker(cleanup_buttons(settings))

            await m.edit_message_text(
                text=cleanup_text.format(
                    chat=m.message.chat.title,
                    cleanup=timehelper.readableTime(
                        timehelper.seconds_to_time(settings["cleanup"])
                    )
                    if settings.get("cleanup", "false") != "false"
                    else "Disabled",
                    cleanup_commands=(
                        "Enabled"
                        if autobool(settings.get("cleanup_commands", False))["bool"]
                        else "Disabled"
                    ),
                    afk_media=(
                        "Enabled"
                        if autobool(settings.get("afk_media", True))["bool"]
                        else "Disabled"
                    ),
                    lang=settings.get("lang", "en"),
                ),
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons),
            )

        else:

            await m.answer("You are not an admin of this group", show_alert=True)

    elif param[0] == "time":

        if m.from_user.id in await get_admins(c, m.message.chat.id):

            if param[1] == "false":

                settings = groupsettings.setting(m.message.chat.id, "cleanup", param[1])
                buttons = settingshelper.btn_maker(cleanup_buttons(settings))

                await m.answer("Chat cleanup disabled")

                await m.edit_message_text(
                    text=cleanup_text.format(
                        chat=m.message.chat.title,
                        cleanup=timehelper.readableTime(
                            timehelper.seconds_to_time(settings["cleanup"])
                        )
                        if settings.get("cleanup", "false") != "false"
                        else "Disabled",
                        cleanup_commands=(
                            "Enabled"
                            if autobool(settings.get("cleanup_commands", False))["bool"]
                            else "Disabled"
                        ),
                        afk_media=(
                            "Enabled"
                            if autobool(settings.get("afk_media", True))["bool"]
                            else "Disabled"
                        ),
                        lang=settings.get("lang", "en"),
                    ),
                    parse_mode=enums.ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )

            else:

                settings = groupsettings.setting(m.message.chat.id, "cleanup", param[1])
                buttons = settingshelper.btn_maker(cleanup_buttons(settings))

                cleanup_time_formatted = (
                    timehelper.readableTime(
                        timehelper.seconds_to_time(settings["cleanup"])
                    )
                    if settings.get("cleanup", "false")
                    else "Disabled"
                )

                try:

                    await m.edit_message_text(
                        text=cleanup_text.format(
                            chat=m.message.chat.title,
                            cleanup=cleanup_time_formatted,
                            cleanup_commands=(
                                "Enabled"
                                if autobool(settings.get("cleanup_commands", False))[
                                    "bool"
                                ]
                                else "Disabled"
                            ),
                            afk_media=(
                                "Enabled"
                                if autobool(settings.get("afk_media", True))["bool"]
                                else "Disabled"
                            ),
                            lang=settings.get("lang", "en"),
                        ),
                        parse_mode=enums.ParseMode.MARKDOWN,
                        reply_markup=InlineKeyboardMarkup(buttons),
                    )

                except exceptions.bad_request_400.MessageNotModified:
                    await m.answer(
                        "No changes made to duration as it was already set to {}".format(
                            cleanup_time_formatted
                        ),
                        show_alert=True,
                    )

                else:
                    await m.answer(
                        "Changed auto cleanup to {}".format(cleanup_time_formatted)
                    )

        else:

            await m.answer("You are not an admin of this group", show_alert=True)

    elif param[0] == "commands":

        if param[1] == "help":

            await m.answer("Delete /afk commands sent by the user", show_alert=True)

        else:

            if m.from_user.id in await get_admins(c, m.message.chat.id):

                settings = groupsettings.setting(
                    m.message.chat.id, "cleanup_commands", autobool(param[1])["bool"]
                )
                buttons = settingshelper.btn_maker(cleanup_buttons(settings))

                await m.answer(
                    "{} command deletion".format(
                        (
                            "Enabled"
                            if autobool(settings.get("cleanup_commands", False))["bool"]
                            else "Disabled"
                        )
                    )
                )

                await m.edit_message_text(
                    text=cleanup_text.format(
                        chat=m.message.chat.title,
                        cleanup=timehelper.readableTime(
                            timehelper.seconds_to_time(settings["cleanup"])
                        )
                        if settings.get("cleanup", "false") != "false"
                        else "Disabled",
                        cleanup_commands=(
                            "Enabled"
                            if autobool(settings.get("cleanup_commands", False))["bool"]
                            else "Disabled"
                        ),
                        afk_media=(
                            "Enabled"
                            if autobool(settings.get("afk_media", True))["bool"]
                            else "Disabled"
                        ),
                        lang=settings.get("lang", "en"),
                    ),
                    parse_mode=enums.ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )

            else:

                await m.answer("You are not an admin of this group", show_alert=True)

    elif param[0] == "back":

        if m.from_user.id in await get_admins(c, m.message.chat.id):

            settings = groupsettings.find_by_id(m.message.chat.id)
            buttons = settingshelper.btn_maker(group_settings_buttons(settings))

            await m.edit_message_text(
                text=settings_text.format(
                    chat=m.message.chat.title,
                    cleanup=timehelper.readableTime(
                        timehelper.seconds_to_time(settings["cleanup"])
                    )
                    if settings.get("cleanup", "false") != "false"
                    else "Disabled",
                    cleanup_commands=(
                        "Enabled"
                        if autobool(settings.get("cleanup_commands", False))["bool"]
                        else "Disabled"
                    ),
                    afk_media=(
                        "Enabled"
                        if autobool(settings.get("afk_media", True))["bool"]
                        else "Disabled"
                    ),
                    lang=settings.get("lang", "en"),
                ),
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons),
            )

        else:

            await m.answer("You are not an admin of this group", show_alert=True)


@Client.on_callback_query(filters.regex("^afk_media"))
async def afk_media(c, m):

    param = m.data.split("_")[2:][0]

    if param == "help":

        await m.answer(
            "Configure visibility of AFK media in this group\n\nRecommended setting: Enabled",
            show_alert=True,
        )

    else:

        if m.from_user.id in await get_admins(c, m.message.chat.id):

            settings = groupsettings.setting(
                m.message.chat.id, "afk_media", autobool(param)["bool"]
            )
            buttons = settingshelper.btn_maker(group_settings_buttons(settings))

            await m.answer(
                "{data} visibility of AFK media in this group".format(
                    data="Enabled" if autobool(param)["bool"] else "Disabled"
                )
            )

            await m.edit_message_text(
                text=settings_text.format(
                    chat=m.message.chat.title,
                    cleanup=timehelper.readableTime(
                        timehelper.seconds_to_time(settings["cleanup"])
                    )
                    if settings.get("cleanup", "false") != "false"
                    else "Disabled",
                    cleanup_commands=(
                        "Enabled"
                        if autobool(settings.get("cleanup_commands", False))["bool"]
                        else "Disabled"
                    ),
                    afk_media=(
                        "Enabled"
                        if autobool(settings.get("afk_media", True))["bool"]
                        else "Disabled"
                    ),
                    lang=settings.get("lang", "en"),
                ),
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons),
            )

        else:

            await m.answer("You are not an admin of this group", show_alert=True)


adminlist = {}


async def get_admins(c, chatid, cache_time=30):

    adminprops = adminlist.get(chatid, False)

    if not adminprops or adminprops.get("time") + timedelta(
        minutes=cache_time
    ) < datetime.now(timezone.utc):
        fetched_admins= []
        async for usr in c.get_chat_members(chatid):
            fetched_admins.append(usr)

        new_adminlist = [each_admin.user.id for each_admin in fetched_admins]
        adminlist[chatid] = {
            "admins": new_adminlist,
            "time": datetime.now(timezone.utc),
        }

    return adminlist[chatid]["admins"]


def group_settings_buttons(settings):

    return [
        [
            {"text": "Chat cleanup", "callback": "cleanup_help"},
            {"text": "Configure ⚙️", "callback": "cleanup_configure"},
        ],
        [
            {"text": "AFK Media", "callback": "afk_media_help"},
            {
                "text": "Enabled ✅"
                if autobool(settings.get("afk_media", True))["bool"]
                else "Disabled ☑️",
                "callback": f"afk_media_{autobool(not settings.get('afk_media', False))['bool']}",
            },
        ],
    ]


def cleanup_buttons(settings):

    return [
        [
            {
                "text": "Enabled ✅"
                if settings.get("cleanup", "false") != "false"
                else "Disabled ☑️",
                "callback": f"""cleanup_time_{"false" if settings.get('cleanup', 'false') != 'false' else "300"}""",
            }
        ],
        [
            {"text": "5m", "callback": "cleanup_time_300"},
            {"text": "10m", "callback": "cleanup_time_600"},
            {"text": "30m", "callback": "cleanup_time_1800"},
            {"text": "1hr", "callback": "cleanup_time_3600"},
        ],
        [
            {"text": "2hr", "callback": "cleanup_time_7200"},
            {"text": "6hr", "callback": "cleanup_time_21600"},
            {"text": "12hr", "callback": "cleanup_time_43200"},
            {"text": "24hr", "callback": "cleanup_time_86400"},
        ],
        [
            {"text": "Delete commands", "callback": "cleanup_commands_help"},
            {
                "text": "Disabled ☑️"
                if autobool(not settings.get("cleanup_commands", False))["bool"]
                else "Enabled ✅",
                "callback": f"cleanup_commands_{autobool(not settings.get('cleanup_commands', False))['bool']}",
            },
        ],
        [
            {"text": "Back 🔙", "callback": "cleanup_back"},
        ],
    ]
