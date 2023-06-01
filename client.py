import os

from pyrogram.client import Client

configpresent = bool(os.path.exists("config.ini"))

if not configpresent:

    sampleconfig = open("sampleconfig.ini", "r").read()

    configtext = sampleconfig.format(
        api_id=os.environ.get("api_id"),
        api_hash=os.environ.get("api_hash"),
        api_token=os.environ.get("api_token"),
        root=os.environ.get("root"),
        uri=os.environ.get("uri"),
        db_name=os.environ.get("db_name"),
        sudo_users=os.environ.get("sudo_users"),
        sudo_chat=os.environ.get("sudo_chat"),
    )

    with open("config.ini", "w") as configfile:
        configfile.write(configtext)


import configparser

config = configparser.ConfigParser()
config.read("config.ini")
bot = config["tokens"]


# configure pyrogram client from config.ini
client = Client(
    "bot",
    api_id=str(bot["api_id"]),
    api_hash=str(bot["api_hash"]),
    bot_token=str(bot["api_token"]),
    plugins=dict(root=str(config["plugins"]["root"])),
)
