from pymongo import ReturnDocument
from datetime import datetime
from database import db
import re


tgusers = db["tgusers"]


def online_user(from_user):
    param = tgusers.find_one_and_update(
            {"id": from_user.id},
            {
                "$set": {
                    "username": from_user.username,
                    "first_name": from_user.first_name,
                    "last_name": from_user.last_name,
                    "seen": datetime.utcnow(),
                    "afk_status": False,
                    "afk_media": None,
                }
            },
            upsert=True,
            return_document=ReturnDocument.BEFORE
        )

    return param


def afked(from_user, reason = None, media = None):
    tgusers.update_one(
        {"id": from_user.id},
        {
            "$set": {
                "username": from_user.username,
                "first_name": from_user.first_name,
                "last_name": from_user.last_name,
                "afk_status": True,
                "reason": reason,
                "afk_media": media,
                "seen": datetime.utcnow(),
            }
        },
        upsert=True,
    )


def new_botuser(from_user):
    tgusers.update_one(
        {"id": from_user.id},
        {
            "$set": {
                "username": from_user.username,
                "first_name": from_user.first_name,
                "last_name": from_user.last_name,
                "bot_user": True,
            }
        },
        upsert=True,
    )


def find_by_username(username):
    user = tgusers.find_one({"username": re.compile(username, re.IGNORECASE)})
    
    if user and user.get('username') == username:
        return user
    
    else:
        return None


def find_by_id(userid):
    user = tgusers.find_one({"id": userid})
    
    if user.get('id') == userid:
        return user

    else:
        return None


def bot_users():
    return list(tgusers.find({}, {'id': 1, "username": 1, "firstname": 1, "lastname": 1}))