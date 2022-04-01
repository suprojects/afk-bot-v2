from pymongo import ReturnDocument
from datetime import datetime

from database import db

tgusers = db["tgusers"]

def online_user(from_user):
    param = tgusers.find_one_and_update(
            {"id": from_user.id},
            {
                "$set": {
                    "username": from_user.username,
                    "firstname": from_user.first_name,
                    "lastname": from_user.last_name,
                    "seen": datetime.utcnow(),
                    "afk_status": False,
                }
            },
            upsert=True,
            return_document=ReturnDocument.BEFORE
        )
    
    return param

def afked(from_user, reason = None):
    tgusers.update_one(
        {"id": from_user.id},
        {
            "$set": {
                "afk_status": True,
                "reason": reason,
            }
        },
        upsert=True,
    )

def new_botuser(userid):
    tgusers.update_one(
        {"id": from_user.id},
        {
            "$set": {
                "botuser": True,
            }
        },
        upsert=True,
    )

def if_afk(userid):
    return tgusers.find_one({'id': userid})

def bot_users():
    return list(tgusers.find({}, {'id': 1, "username": 1, "firstname": 1, "lastname": 1}))