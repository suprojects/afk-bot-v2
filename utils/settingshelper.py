from pyrogram.types import InlineKeyboardButton


def btn_maker(param):

    buttons = []

    for btnlist in param:
        button_row = [
            InlineKeyboardButton(text=btn["text"], callback_data=btn["callback"])
            for btn in btnlist
        ]
        buttons.append(button_row)

    return buttons
