
'''

from datetime import datetime

from database import db

afkers = db["afkusers"]

def new_afk(from_user):
    afkers.update_one(
        {"id": from_user.id},
        {
            "$set": {
                "username": from_user.username,
                "firstname": from_user.first_name,
                "lastname": from_user.last_name,
                "time": datetime.now(),
            }
        },
        upsert=True,
    )

def del_afk(from_user):
    details = if_afk(from_user)
    afkers.delete_one({"id": from_user.id})
    return details

def if_afk(from_user):
    return afkers.find_one({'id': from_user.id})

def bot_users():
    return list(afkers.find({}, {'id': 1, "username": 1, "firstname": 1, "lastname": 1}))
    
'''