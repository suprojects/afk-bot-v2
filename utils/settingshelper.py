from pyrogram.types import InlineKeyboardButton

def btn_maker(param):
    
    buttons = []
    
    for btnlist in param:
        button_row = []
        
        for btn in btnlist:
            button_row.append(InlineKeyboardButton(text=btn['text'], callback_data=btn['callback']))
        
        buttons.append(button_row)
        
    return buttons