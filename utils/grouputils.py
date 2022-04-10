from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client

async def cleanup(message, time=5):
    
    async def delete(message): await message.delete()
    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(await delete(message), "interval", seconds=time)

    scheduler.start()