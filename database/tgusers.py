import re
from datetime import datetime, timezone
from pymongo import ReturnDocument

from database import db

tgusers = db["tgusers"]


def online_user(from_user):
    return tgusers.find_one_and_update(
        {"id": from_user.id},
        {
            "$set": {
                "username": from_user.username,
                "first_name": from_user.first_name,
                "last_name": from_user.last_name,
                "seen": datetime.now(timezone.utc),
                "afk_status": False,
                "afk_media": None,
            }
        },
        upsert=True,
        return_document=ReturnDocument.BEFORE,
    )


def afked(from_user, reason=None, media=None):
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
                "seen": datetime.now(timezone.utc),
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

    if user and user.get("username").lower() == username.lower():
        return user

    else:
        return None


def find_by_id(userid):
    user = tgusers.find_one({"id": userid})

    return user if user and user.get("id") == userid else None


def bot_users():
    return list(
        tgusers.find({}, {"id": 1, "username": 1, "firstname": 1, "lastname": 1})
    )
