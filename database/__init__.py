import configparser

from pymongo import MongoClient

config = configparser.ConfigParser()
config.read("config.ini")
database = config["database"]

import certifi

ca = certifi.where()

client = MongoClient(database["uri"], tlsCAFile=ca)
db = client[database["db_name"]]
