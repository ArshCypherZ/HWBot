# Code Fixed By Moezilla

import asyncio
from Himawari.utils.permissions import adminsOnly
from Himawari import pgram as app, OWNER_ID, db
from Himawari.utils.errors import capture_err
from Himawari.modules.mongo.karma_mongo import (
    alpha_to_int,
    get_karma,
    get_karmas,
    int_to_alpha,
    is_karma_on,
    karma_off,
    karma_on,
    update_karma,
)
from pyrogram import filters


regex_upvote = r"^((?i)\+|\+\+|\+1|thx|tnx|ty|thank you|thanx|thanks|pro|cool|good|👍|nice|noice|piro)$"
regex_downvote = r"^(\-|\-\-|\-1|👎|noob|Noob|gross|fuck off)$"

karma_positive_group = 3
karma_negative_group = 4


from Himawari import MONGO_DB_URL

from pymongo import MongoClient

worddb = MongoClient(MONGO_DB_URL) 
k = worddb["Himalol"]["karma_toggle"]

 


async def is_admins(chat_id: int):
    return [
        member.user.id
        async for member in app.iter_chat_members(
            chat_id, filter="administrators"
        )
    ]





@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_upvote)
    & ~filters.via_bot
    & ~filters.bot,
    group=karma_positive_group,
)
async def upvote(_, message):
    chat_id = message.chat.id
    is_karma = k.find_one({"chat_id": chat_id})    
    if not is_karma:
        if not message.reply_to_message.from_user:
            return
        if not message.from_user:
            return
        if message.reply_to_message.from_user.id == message.from_user.id:
            return
        user_id = message.reply_to_message.from_user.id
        user_mention = message.reply_to_message.from_user.mention
        current_karma = await get_karma(
            chat_id, await int_to_alpha(user_id)
        )
        if current_karma:
            current_karma = current_karma['karma']
            karma = current_karma + 1
        else:
            karma = 1
        new_karma = {"karma": karma}
        await update_karma(
            chat_id, await int_to_alpha(user_id), new_karma
        )
        await message.reply_text(
            f"Incremented Karma of {user_mention} By 1 \nTotal Points: {karma}"
        )

@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_downvote)
    & ~filters.via_bot
    & ~filters.bot,
    group=karma_negative_group,
)
async def downvote(_, message):
    chat_id = message.chat.id
    is_karma = k.find_one({"chat_id": chat_id})    
    if is_karma:
        if not message.reply_to_message.from_user:
            return
        if not message.from_user:
            return
        if message.reply_to_message.from_user.id == message.from_user.id:
            return
        user_id = message.reply_to_message.from_user.id
        user_mention = message.reply_to_message.from_user.mention
        current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
        if current_karma:
            current_karma = current_karma["karma"]
            karma = current_karma - 1
        else:
            karma = 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
        await message.reply_text(
            f"Decremented Karma Of {user_mention} By 1 \nTotal Points: {karma}"
        )


@app.on_message(filters.command("karmastats") & filters.group)
@capture_err
async def karma(_, message):
    chat_id = message.chat.id
    if not message.reply_to_message:
        m = await message.reply_text("Analyzing Karma...Will Take 10 Seconds")
        karma = await get_karmas(chat_id)
        if not karma:
            await m.edit("No karma in DB for this chat.")
            return
        msg = f"**Karma list of {message.chat.title}:- **\n"
        limit = 0
        karma_dicc = {}
        for i in karma:
            user_id = await alpha_to_int(i)
            user_karma = karma[i]["karma"]
            karma_dicc[str(user_id)] = user_karma
            karma_arranged = dict(
                sorted(karma_dicc.items(), key=lambda item: item[1], reverse=True)
            )
        if not karma_dicc:
            await m.edit("No karma in DB for this chat.")
            return
        for user_idd, karma_count in karma_arranged.items():
            if limit > 9:
                break
            try:
                user = await app.get_users(int(user_idd))
                await asyncio.sleep(0.8)
            except Exception:
                continue
            first_name = user.first_name
            if not first_name:
                continue
            username = user.username
            msg += f"**{karma_count}**  {(first_name[0:12] + '...') if len(first_name) > 12 else first_name}  `{('@' + username) if username else user_idd}`\n"
            limit += 1
        await m.edit(msg)
    else:
        user_id = message.reply_to_message.from_user.id
        karma = await get_karma(chat_id, await int_to_alpha(user_id))
        karma = karma["karma"] if karma else 0
        await message.reply_text(f"**Total Point :** {karma}")




__mod_name__ = "Karma"
__help__ = """

*Upvote* - Use upvote keywords like "+", "+1", "thanks", etc. to upvote a message.
*Downvote* - Use downvote keywords like "-", "-1", etc. to downvote a message.

*Commands*
•/karmastats:- reply to a user to check that user's karma points.
•/karmastats:- send without replying to any message to check karma point list of top 10
•/karma :- Enable/Disable karma in your group.
"""
