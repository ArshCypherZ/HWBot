"""
MIT License

Copyright (c) 2022 Arsh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os

from telethon.tl.types import ChatBannedRights
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telethon import functions
from telethon import types

from Himawari import telethn as tbot, dispatcher
from Himawari.events import register
from Himawari.modules.sql.nightmode_sql import (
    add_nightmode,
    rmnightmode,
    get_all_chat_id,
    is_nightmode_indb,
)


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    elif isinstance(chat, types.InputPeerChat):

        ui = await tbot.get_peer_id(user)
        ps = (
            await tbot(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    else:
        return None


hima = ChatBannedRights(
    until_date=None,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    send_polls=True,
    invite_users=True,
    pin_messages=True,
    change_info=True,
)
openhima = ChatBannedRights(
    until_date=None,
    send_messages=False,
    send_media=False,
    send_stickers=False,
    send_gifs=False,
    send_games=False,
    send_inline=False,
    send_polls=False,
    invite_users=True,
    pin_messages=True,
    change_info=True,
)


@register(pattern="^/nightmode")
async def close_ws(event):
    if event.is_group:
        if not (await is_register_admin(event.input_chat, event.message.sender_id)):
            await event.reply("You are not admin so you can't use this command...")
            return

    if not event.is_group:
        await event.reply("You Can Only Enable Night Mode in Groups.")
        return
    if is_nightmode_indb(str(event.chat_id)):
        await event.reply("This Chat Has Already Enabled Night Mode.")
        return
    add_nightmode(str(event.chat_id))
    await event.reply(
        f"Added Chat {event.chat.title} With ID `{event.chat_id}` To Database. **This Group Will Be Closed On 12 AM (IST) And Will Open On 06 AM (IST)**"
    )


@register(pattern="^/rmnight")
async def disable_ws(event):
    if event.is_group:
        if not (await is_register_admin(event.input_chat, event.message.sender_id)):
            await event.reply("You are not admin so you can't use this command...")
            return

    if not event.is_group:
        await event.reply("You Can Only Disable Night Mode in Groups.")
        return
    if not is_nightmode_indb(str(event.chat_id)):
        await event.reply("This Chat Has Not Enabled Night Mode.")
        return
    rmnightmode(str(event.chat_id))
    await event.reply(
        f"Removed Chat {event.chat.title} With ID `{event.chat_id}` From Database."
    )


async def job_close():
    ws_chats = get_all_chat_id()
    if len(ws_chats) == 0:
        return
    for warner in ws_chats:
        try:
            await tbot.send_message(
                int(warner.chat_id),
                f"12:00 AM, Group Is Closing Till 6 Am. Night Mode Started ! \n**Powered By {dispatcher.bot.username} **",
            )
            await tbot(
                functions.messages.EditChatDefaultBannedRightsRequest(
                    peer=int(warner.chat_id), banned_rights=hima
                )
            )
        except Exception as e:
            logger.info(f"Unable To Close Group {warner} - {e}")


# Run everyday at 12am
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_close, trigger="cron", hour=23, minute=59)
scheduler.start()


async def job_open():
    ws_chats = get_all_chat_id()
    if len(ws_chats) == 0:
        return
    for warner in ws_chats:
        try:
            await tbot.send_message(
                int(warner.chat_id),
                f"06:00 AM, Group Is Opening.\n**Powered By {dispatcher.bot.username}**",
            )
            await tbot(
                functions.messages.EditChatDefaultBannedRightsRequest(
                    peer=int(warner.chat_id), banned_rights=openhima
                )
            )
        except Exception as e:
            logger.info(f"Unable To Open Group {warner.chat_id} - {e}")


# Run everyday at 06
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(job_open, trigger="cron", hour=6, minute=1)
scheduler.start()

__help__ = """
*Admins Only*

• /nightmode*:* Adds Group to NightMode Chats
• /rmnight*:* Removes Group From NightMode Chats

*Note:* Night Mode chats get Automatically closed at 12 am (IST) and Automatically opens at 6 am (IST) to Prevent Night Spams.
"""

__mod_name__ = "Night Mode"