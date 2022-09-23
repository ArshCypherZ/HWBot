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

import html
import requests
import nekos

from Himawari import dispatcher
import Himawari.modules.sql.nsfw_sql as sql
from Himawari.modules.log_channel import gloggable
from telegram import Update
from telegram.error import BadRequest, RetryAfter, Unauthorized
from telegram.ext import CommandHandler, CallbackContext
from Himawari.modules.helper_funcs.filters import CustomFilters
from Himawari.modules.helper_funcs.chat_status import user_admin
from telegram.utils.helpers import mention_html

url_nsfw = "https://api.waifu.pics/nsfw/"

@user_admin
@gloggable
def add_nsfw(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    is_nsfw = sql.is_nsfw(chat.id)
    if not is_nsfw:
        sql.set_nsfw(chat.id)
        msg.reply_text("Activated NSFW Mode!")
        message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"ACTIVATED_NSFW\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        )
        return message
    else:
        msg.reply_text("NSFW Mode is already Activated for this chat!")
        return ""

@user_admin
@gloggable
def rem_nsfw(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    is_nsfw = sql.is_nsfw(chat.id)
    if not is_nsfw:
        msg.reply_text("NSFW Mode is already Deactivated")
        return ""
    else:
        sql.rem_nsfw(chat.id)
        msg.reply_text("Rolled Back to SFW Mode!")
        message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"DEACTIVATED_NSFW\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        )
        return message

def list_nsfw_chats(update: Update, context: CallbackContext):
    chats = sql.get_all_nsfw_chats()
    text = "<b>NSFW Activated Chats</b>\n"
    for chat in chats:
        try:
            x = context.bot.get_chat(int(*chat))
            name = x.title if x.title else x.first_name
            text += f"• <code>{name}</code>\n"
        except BadRequest:
            sql.rem_nsfw(*chat)
        except Unauthorized:
            sql.rem_nsfw(*chat)
        except RetryAfter as e:
            sleep(e.retry_after)
    update.effective_message.reply_text(text, parse_mode="HTML")

def blowjob(update, context):
    chat_id = update.effective_chat.id
    if not update.effective_message.chat.type == "private":
        is_nsfw = sql.is_nsfw(chat_id)
        if not is_nsfw:
            msg.reply_text("NSFW is not activated")
            return
    msg = update.effective_message
    url = f"{url_nsfw}blowjob" 
    result = requests.get(url).json()
    img = result['url']
    msg.reply_animation(img)

def trap(update, context):
    chat_id = update.effective_chat.id
    if not update.effective_message.chat.type == "private":
        is_nsfw = sql.is_nsfw(chat_id)
        if not is_nsfw:
            msg.reply_text("NSFW is not activated")
            return
    msg = update.effective_message
    url = f"{url_nsfw}trap" 
    result = requests.get(url).json()
    img = result['url']
    msg.reply_photo(photo=img)

def nsfwwaifu(update, context):
    chat_id = update.effective_chat.id
    if not update.effective_message.chat.type == "private":
        is_nsfw = sql.is_nsfw(chat_id)
        if not is_nsfw:
            msg.reply_text("NSFW is not activated")
            return
    msg = update.effective_message
    url = f"{url_nsfw}waifu" 
    result = requests.get(url).json()
    img = result['url']
    msg.reply_photo(photo=img)

def nsfwneko(update, context):
    chat_id = update.effective_chat.id
    if not update.effective_message.chat.type == "private":
        is_nsfw = sql.is_nsfw(chat_id)
        if not is_nsfw:
            msg.reply_text("NSFW is not activated")
            return
    msg = update.effective_message
    url = f"{url_nsfw}neko" 
    result = requests.get(url).json()
    img = result['url']
    msg.reply_photo(photo=img)

def spank(update, context):
    chat_id = update.effective_chat.id
    if not update.effective_message.chat.type == "private":
        is_nsfw = sql.is_nsfw(chat_id)
        if not is_nsfw:
            return
    msg = update.effective_message
    target = "spank"
    msg.reply_animation(nekos.img(target))

ADD_NSFW_HANDLER = CommandHandler("addnsfw", add_nsfw)
REMOVE_NSFW_HANDLER = CommandHandler("rmnsfw", rem_nsfw)
LIST_NSFW_CHATS_HANDLER = CommandHandler(
    "nsfwchats", list_nsfw_chats, filters=CustomFilters.dev_filter)
NSFWWAIFU_HANDLER = CommandHandler(("nsfwwaifu", "nwaifu"), nsfwwaifu, run_async=True)
BLOWJOB_HANDLER = CommandHandler(("blowjob", "bj"), blowjob, run_async=True)
TRAP_HANDLER = CommandHandler("trap", trap, run_async=True)
NSFWNEKO_HANDLER = CommandHandler(("nsfwneko", "nneko"), nsfwneko, run_async=True)
SPANK_HANDLER = CommandHandler("spank", spank, run_async=True)

dispatcher.add_handler(ADD_NSFW_HANDLER)
dispatcher.add_handler(REMOVE_NSFW_HANDLER)
dispatcher.add_handler(LIST_NSFW_CHATS_HANDLER)
dispatcher.add_handler(NSFWWAIFU_HANDLER)
dispatcher.add_handler(BLOWJOB_HANDLER)
dispatcher.add_handler(SPANK_HANDLER)
dispatcher.add_handler(TRAP_HANDLER)
dispatcher.add_handler(NSFWNEKO_HANDLER)

__handlers__ = [
    ADD_NSFW_HANDLER,
    REMOVE_NSFW_HANDLER,
    LIST_NSFW_CHATS_HANDLER,
    ADD_NSFW_HANDLER,
    REMOVE_NSFW_HANDLER,
    LIST_NSFW_CHATS_HANDLER,
    NSFWWAIFU_HANDLER,
    SPANK_HANDLER,
    BLOWJOB_HANDLER,
    TRAP_HANDLER,
    NSFWNEKO_HANDLER
]



__mod_name__ = "NSFW"

__help__ = """
• `/addnsfw` : To Activate NSFW commands.
• `/rmnsfw` : To Deactivate NSFW commands.

Following are the NSFW commands:

• `/nsfwwaifu`
• `/blowjob`
• `/nwaifu`
• `/bj`
• `/trap`
• `/nsfwneko`
• `/nneko`
• `/spank`
"""