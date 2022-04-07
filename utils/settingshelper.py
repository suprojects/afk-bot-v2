from pyrogram.types import InlineKeyboardButton

def pvt_settings_buttons(param):
    
    buttons = []
    
    for btnlist in param:
        button_row = []
        
        for btn in btnlist:
            button_row.append(InlineKeyboardButton(text=btn['text'], callback_data=btn['callback']))
        
        buttons.append(button_row)
        
    return buttons

def btn_maker(settings):
    btn = [
        [
            {'text': 'Time Hider', 'callback': 'privacy_time_help'},
            {'text': 'Enabled ✅' if (settings.get('privacy_time', False)) else 'Disabled ❌', 'callback': 'privacy_time_{}'.format(str(not (settings.get('privacy_time', False))).lower())}
        ],
        [
            {'text': 'Seen Hider', 'callback': 'privacy_seen_help'},
            {'text': 'Enabled ✅' if (settings.get('privacy_seen', False)) else 'Disabled ❌', 'callback': 'privacy_seen_{}'.format(str(not (settings.get('privacy_seen', False))).lower())}

        ],
        [
            {'text': 'Mention Logger', 'callback': 'mention_log_help'},
            {'text': 'Enabled ✅' if (settings.get('mention_log', False)) else 'Disabled ❌', 'callback': 'mention_log_{}'.format(str(not (settings.get('mention_log', False))).lower())}

        ]
    ]
    
    return btn