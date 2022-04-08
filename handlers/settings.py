from pyrogram import Client, filters

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import tgusers, pvtsettings

from utils import settingshelper
from distutils.util import strtobool


settings_text = """

Current settings for {mention}:

Time hider: **{privacy_time}**
Seen hider: **{privacy_seen}**
Mention Logger: **{mention_log}**

Language: **{lang}**

__Click the buttons to learn about the settings__

"""



@Client.on_message(filters.command('settings') & filters.private)

async def settings_pvt(c,m):
    settings = tgusers.find_by_id(m.from_user.id)

    buttons = settingshelper.btn_maker(settingshelper.pvt_settings_btns(settings))
    
    await m.reply(settings_text.format(

        mention=f'[{m.from_user.first_name}](tg://user?id={m.from_user.id})',
        privacy_time=("Enabled" if settings.get('privacy_time', False) else "Disabled"),
        privacy_seen=("Enabled" if settings.get('privacy_seen', False) else "Disabled"),
        mention_log= ("Enabled" if settings.get('mention_log', False) else "Disabled"),
        lang=settings.get('lang', 'en'),

), parse_mode='markdown', reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex('^privacy_time'))

async def timeprivacy(c,m):

    param = m.data.split('_')[2:][0]


    if param == 'help': await m.answer("Hides the duration you were AFK in reply messages", show_alert=True)

    else: 
        
        settings = pvtsettings.setting(m.from_user, 'privacy_time', bool(strtobool(param)))
        
        buttons = settingshelper.btn_maker(settingshelper.pvt_settings_btns(settings))
        
        await m.answer('{data} Time hider'.format(data="Enabled" if bool(strtobool(param)) else "Disabled"), show_alert=True)
        
        await c.edit_message_text(
            chat_id = m.from_user.id,
            message_id = m.message.message_id,
            text=settings_text.format(
                mention=f'[{m.from_user.first_name}](tg://user?id={m.from_user.id})',
                privacy_time=settings.get('privacy_time', False),
                privacy_seen=settings.get('privacy_seen', False),
                mention_log=settings.get('mention_log', False),
                lang=settings.get('lang', 'en'),
                
            ), parse_mode='markdown', reply_markup=InlineKeyboardMarkup(buttons)
        )


@Client.on_callback_query(filters.regex('^privacy_seen'))

async def seenprivacy(c,m):

    param = m.data.split('_')[2:][0]


    if param == 'help': await m.answer("Disables /seen command to be used on your account", show_alert=True)

    else: 

        settings = pvtsettings.setting(m.from_user, 'privacy_seen', bool(strtobool(param)))
        
        buttons = settingshelper.btn_maker(settingshelper.pvt_settings_btns(settings))
        
        await m.answer('{data} Seen hider'.format(data="Enabled" if bool(strtobool(param)) else "Disabled"), show_alert=True)
        
        await c.edit_message_text(
            chat_id = m.from_user.id,
            message_id = m.message.message_id,
            text=settings_text.format(
                mention=f'[{m.from_user.first_name}](tg://user?id={m.from_user.id})',
                privacy_time=settings.get('privacy_time', False),
                privacy_seen=settings.get('privacy_seen', False),
                mention_log=settings.get('mention_log', False),
                lang=settings.get('lang', 'en'),
                
            ), parse_mode='markdown', reply_markup=InlineKeyboardMarkup(buttons)
        )


@Client.on_callback_query(filters.regex('^mention_log'))

async def mentionlogger(c,m):

    param = m.data.split('_')[2:][0]


    if param == 'help': await m.answer("Sends you a PM for any mentions you get", show_alert=True)

    else: 

        settings = pvtsettings.setting(m.from_user, 'mention_log', bool(strtobool(param)))
        
        buttons = settingshelper.btn_maker(settingshelper.pvt_settings_btns(settings))
        
        await m.answer('{data} Mention Logger'.format(data="Enabled" if bool(strtobool(param)) else "Disabled"), show_alert=True)
        
        await c.edit_message_text(
            chat_id = m.from_user.id,
            message_id = m.message.message_id,
            text=settings_text.format(
                mention=f'[{m.from_user.first_name}](tg://user?id={m.from_user.id})',
                privacy_time=settings.get('privacy_time', False),
                privacy_seen=settings.get('privacy_seen', False),
                mention_log=settings.get('mention_log', False),
                lang=settings.get('lang', 'en'),
                
            ), parse_mode='markdown', reply_markup=InlineKeyboardMarkup(buttons)
        )