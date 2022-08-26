# Made By Moezilla

import asyncio
from Himawari import pgram as app, OWNER_ID, db
from Himawari.utils.errors import capture_err
from pyrogram import *
from pyrogram.types import *
import Himawari.modules.sql.users_sql as sql

from Himawari import MONGO_DB_URL

from pymongo import MongoClient

worddb = MongoClient(MONGO_DB_URL) 
k = worddb["Himalol"]["live_stats"]


@app.on_message(
    filters.text
    & ~filters.private,
)
async def live(client: Client, message: Message):
    is_live = k.find_one({"live": "stats"})
    users = f"{sql.num_users()}"
    chats = f"{sql.num_chats()}"
    captionk =  f"Live Himawari Stats\n\n• {sql.num_users()} users, across {sql.num_chats()} chats"
    if not is_live:     
        k.insert_one({"live": "stats", "user": users, "chat": chats})
        await app.edit_message_text(chat_id=-1001749357191, message_id=20, text=captionk, disable_web_page_preview=True)
    if is_live:       
        is_live2 = k.find_one({"live": "stats", "user": users, "chat": chats})
        if not is_live2:       
            k.update_one({"live": "stats"}, {"$set": {"user": users, "chat": chats}})
            # editing chat_id and message id
            await app.edit_message_text(chat_id=-1001749357191, message_id=20, text=captionk, disable_web_page_preview=True)
   
  
