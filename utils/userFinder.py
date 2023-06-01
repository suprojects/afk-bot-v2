import re

from database import tgusers


def find(attr):

    if attr == "@":
        return None

    elif attr.isdecimal():
        return tgusers.find_by_id(int(attr))

    elif re.search("^@[a-zA-Z0-9_]*$", attr):
        return tgusers.find_by_username(attr[1:])

    else:
        return None
