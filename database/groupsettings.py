from pymongo import ReturnDocument

from database import db

from utils.chattypeHelper import chatTypeConv

bot_chats = db["bot_chats"]

def setting(chatid, setting, data):

    param = bot_chats.find_one_and_update(
        {"id": chatid},
        {
            "$set": {
                setting: data,
            }
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return param


def new_chat(chat):

    bot_chats.update_one(
        {"id": chat.id},
        {
            "$set": {
                "title": chat.title,
                "username": chat.username,
                "dc_id": chat.dc_id,
                "type": chatTypeConv(chat.type),
            }
        },
        upsert=True,
    )


def find_by_id(chatid):

    return bot_chats.find_one({"id": chatid})
