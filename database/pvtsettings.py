from pymongo import ReturnDocument

from database import db

tgusers = db["tgusers"]


def setting(from_user, setting, data):
    param = tgusers.find_one_and_update(
        {"id": from_user.id},
        {
            "$set": {
                setting: data,
            }
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return param
