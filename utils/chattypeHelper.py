from pyrogram import enums


def chatTypeConv(type):
    if type == enums.ChatType.SUPERGROUP:
        return str("supergroup")

    elif type == enums.ChatType.GROUP:
        return str("group")

    elif type == enums.ChatType.CHANNEL:
        return str("channel")

    elif type == enums.ChatType.PRIVATE:
        return str("private")

    elif type == enums.ChatType.BOT:
        return str("bot")
