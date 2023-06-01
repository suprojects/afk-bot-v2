from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram.errors import exceptions

from client import client
from database import groupsettings

deleteList = []


def newDeleteJob(chat_id, message_id, delete_command=False, command_id=None, delete_delay=300):

    deleteList.append(
        {
            "chat_id": chat_id,
            "message_id": message_id,
            "delete_command": delete_command,
            "command_id": command_id,
            "time": datetime.now(timezone.utc) + timedelta(seconds=int(delete_delay)),
        }
    )


async def checkJobs():

    for job in deleteList:

        if job["time"] < datetime.now(timezone.utc):

            await client.delete_messages(
                chat_id=job["chat_id"], message_ids=job["message_id"]
            )

            if job["delete_command"] and job["command_id"]:

                try:
                    await client.delete_messages(
                        chat_id=job["chat_id"], message_ids=job["command_id"]
                    )

                except exceptions.forbidden_403.MessageDeleteForbidden:
                    groupsettings.setting(job["chat_id"], "cleanup_commands", False)

            deleteList.remove(job)


def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(checkJobs, "interval", seconds=60)
    scheduler.start()
