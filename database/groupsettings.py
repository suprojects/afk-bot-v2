from pymongo import ReturnDocument
from database import db

bot_chats = db["bot_chats"]

def setting(chat, setting, data):
    
    param = bot_chats.find_one_and_update(
            {"id": chat.id},
            {
                "$set": {
                    setting: data,
                }
            },
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
    return param


def new_chat(chat):
    
    bot_chats.update_one(
        {"id": chat.id},
        {
            "$set": {
                "username": chat.username,
                "title": chat.title,
                "username": chat.username,
                "dc_id": chat.dc_id,
                "type": chat.type,
            }
        },
            upsert=True,
        )
    

def find_by_id(chatid):
    
    return bot_chats.find_one({"id": chatid})
