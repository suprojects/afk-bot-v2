from client import client
from utils.autoDelete import start_scheduler

start_scheduler()
client.run()
