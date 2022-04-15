from database import tgusers
import re

def find(attr):
    
    if attr == '@':
        userinfo = None
        
    elif attr.isdecimal():
        userinfo = tgusers.find_by_id(int(attr))

    elif re.search("^@[a-zA-Z0-9_]*$", attr):
        userinfo = tgusers.find_by_username(attr[1:])

    else:
        userinfo = None

    return userinfo