from pyrogram import enums, filters
from pyrogram.client import Client
from pyrogram.types import InlineKeyboardMarkup

from database import pvtsettings, tgusers
from utils import settingshelper
from utils.formatutils import autobool

settings_text = """
Current settings for {mention}:

Time hider: **{privacy_time}**
Seen hider: **{privacy_seen}**
Mention Logger: **{mention_log}**

Language: **{lang}**

__Click the buttons to learn about the settings__

"""


@Client.on_message(filters.command("settings") & filters.private)
async def settings_pvt(c, m):
    settings = tgusers.find_by_id(m.from_user.id)

    if settings:
        buttons = settingshelper.btn_maker(pvt_settings_buttons(settings))

    else:
        await m.reply("Please start the bot first by using /start command")
        return

    await m.reply(
        settings_text.format(
            mention=f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})",
            privacy_time=(
                "Enabled"
                if autobool(settings.get("privacy_time", False))["bool"]
                else "Disabled"
            ),
            privacy_seen=(
                "Enabled"
                if autobool(settings.get("privacy_seen", False))["bool"]
                else "Disabled"
            ),
            mention_log=(
                "Enabled"
                if autobool(settings.get("mention_log", False))["bool"]
                else "Disabled"
            ),
            lang=settings.get("lang", "en"),
        ),
        parse_mode=enums.ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@Client.on_callback_query(filters.regex("^privacy_time"))
async def timeprivacy(c, m):
    param = m.data.split("_")[2:][0]

    if param == "help":
        await m.answer(
            "Hides the duration you were AFK in reply messages", show_alert=True
        )

    else:
        settings = pvtsettings.setting(
            m.from_user, "privacy_time", autobool(param)["bool"]
        )

        buttons = settingshelper.btn_maker(pvt_settings_buttons(settings))

        await m.answer(
            "{data} Time hider".format(
                data="Enabled" if autobool(param)["bool"] else "Disabled"
            )
        )

        await m.message.edit(
            text=settings_text.format(
                mention=f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})",
                privacy_time=(
                    "Enabled"
                    if autobool(settings.get("privacy_time", False))["bool"]
                    else "Disabled"
                ),
                privacy_seen=(
                    "Enabled"
                    if autobool(settings.get("privacy_seen", False))["bool"]
                    else "Disabled"
                ),
                mention_log=(
                    "Enabled"
                    if autobool(settings.get("mention_log", False))["bool"]
                    else "Disabled"
                ),
                lang=settings.get("lang", "en"),
            ),
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@Client.on_callback_query(filters.regex("^privacy_seen"))
async def seenprivacy(c, m):
    param = m.data.split("_")[2:][0]

    if param == "help":
        await m.answer(
            "Disables /seen command to be used on your account", show_alert=True
        )

    else:
        settings = pvtsettings.setting(
            m.from_user, "privacy_seen", autobool(param)["bool"]
        )

        buttons = settingshelper.btn_maker(pvt_settings_buttons(settings))

        await m.answer(
            "{data} Seen hider".format(
                data="Enabled" if autobool(param)["bool"] else "Disabled"
            )
        )

        await m.message.edit(
            text=settings_text.format(
                mention=f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})",
                privacy_time=(
                    "Enabled"
                    if autobool(settings.get("privacy_time", False))["bool"]
                    else "Disabled"
                ),
                privacy_seen=(
                    "Enabled"
                    if autobool(settings.get("privacy_seen", False))["bool"]
                    else "Disabled"
                ),
                mention_log=(
                    "Enabled"
                    if autobool(settings.get("mention_log", False))["bool"]
                    else "Disabled"
                ),
                lang=settings.get("lang", "en"),
            ),
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@Client.on_callback_query(filters.regex("^mention_log"))
async def mentionlogger(c, m):
    param = m.data.split("_")[2:][0]

    if param == "help":
        await m.answer("Sends you a PM for any mentions you get", show_alert=True)

    else:
        settings = pvtsettings.setting(
            m.from_user, "mention_log", autobool(param)["bool"]
        )

        buttons = settingshelper.btn_maker(pvt_settings_buttons(settings))

        await m.answer(
            "{data} Mention Logger".format(
                data="Enabled" if autobool(param)["bool"] else "Disabled"
            )
        )

        await m.message.edit(
            text=settings_text.format(
                mention=f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})",
                privacy_time=(
                    "Enabled"
                    if autobool(settings.get("privacy_time", False))["bool"]
                    else "Disabled"
                ),
                privacy_seen=(
                    "Enabled"
                    if autobool(settings.get("privacy_seen", False))["bool"]
                    else "Disabled"
                ),
                mention_log=(
                    "Enabled"
                    if autobool(settings.get("mention_log", False))["bool"]
                    else "Disabled"
                ),
                lang=settings.get("lang", "en"),
            ),
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


def pvt_settings_buttons(settings):
    return [
        [
            {"text": "Time Hider", "callback": "privacy_time_help"},
            {
                "text": "Disabled ☑️"
                if autobool(not settings.get("privacy_time", False))["bool"]
                else "Enabled ✅",
                "callback": f"privacy_time_{autobool(not settings.get('privacy_time', False))['bool']}",
            },
        ],
        [
            {"text": "Seen Hider", "callback": "privacy_seen_help"},
            {
                "text": "Disabled ☑️"
                if autobool(not settings.get("privacy_seen", False))["bool"]
                else "Enabled ✅",
                "callback": f"privacy_seen_{autobool(not settings.get('privacy_seen', False))['bool']}",
            },
        ],
        [
            {"text": "Mention Logger", "callback": "mention_log_help"},
            {
                "text": "Disabled ☑️"
                if autobool(not settings.get("mention_log", False))["bool"]
                else "Enabled ✅",
                "callback": f"mention_log_{autobool(not settings.get('mention_log', False))['bool']}",
            },
        ],
    ]
