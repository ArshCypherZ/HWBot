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
from typing import Optional
from datetime import timedelta
from pytimeparse.timeparse import timeparse

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext
from telegram.utils.helpers import mention_html

from Himawari.modules.log_channel import loggable
from Himawari.modules.helper_funcs.anonymous import user_admin, AdminPerms
from Himawari.modules.helper_funcs.chat_status import bot_admin, connection_status, user_admin_no_reply
from Himawari.modules.helper_funcs.decorators import Himawaricmd, Himawaricallback
from Himawari import LOGGER, updater

import Himawari.modules.sql.welcome_sql as sql

j = updater.job_queue

# store job id in a dict to be able to cancel them later
RUNNING_RAIDS = {}  # {chat_id:job_id, ...}


def get_time(time: str) -> int:
    try:
        return timeparse(time)
    except BaseException:
        return 0


def get_readable_time(time: int) -> str:
    t = f"{timedelta(seconds=time)}".split(":")
    if time == 86400:
        return "1 day"
    return f"{t[0]} hour(s)" if time >= 3600 else f"{t[1]} minutes"


@Himawaricmd(command="raid", pass_args=True)
@bot_admin
@connection_status
@loggable
@user_admin(AdminPerms.CAN_CHANGE_INFO)
def setRaid(update: Update, context: CallbackContext) -> Optional[str]:
    args = context.args
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    if chat.type == "private":
        context.bot.sendMessage(chat.id, "This command is not available in PMs.")
        return
    stat, time, acttime = sql.getRaidStatus(chat.id)
    readable_time = get_readable_time(time)
    if len(args) == 0:
        if stat:
            text = 'Raid mode is currently <code>Enabled</code>\nWould you like to <code>Disable</code> raid?'
            keyboard = [
                [
                    InlineKeyboardButton(
                        "Disable Raid Mode",
                        callback_data=f"disable_raid={chat.id}={time}",
                    ),
                    InlineKeyboardButton(
                        "Cancel Action", callback_data="cancel_raid=1"
                    ),
                ]
            ]

        else:
            text = f"Raid mode is currently <code>Disabled</code>\nWould you like to <code>Enable</code> " \
                   f"raid for {readable_time}?"
            keyboard = [
                [
                    InlineKeyboardButton(
                        "Enable Raid Mode",
                        callback_data=f"enable_raid={chat.id}={time}",
                    ),
                    InlineKeyboardButton(
                        "Cancel Action", callback_data="cancel_raid=0"
                    ),
                ]
            ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        msg.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

    elif args[0] == "off":
        if stat:
            sql.setRaidStatus(chat.id, False, time, acttime)
            j.scheduler.remove_job(RUNNING_RAIDS.pop(chat.id))
            text = "Raid mode has been <code>Disabled</code>, members that join will no longer be kicked."
            msg.reply_text(text, parse_mode=ParseMode.HTML)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#RAID\n"
                f"Disabled\n"
                f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n")

    else:
        args_time = args[0].lower()
        if time := get_time(args_time):
            readable_time = get_readable_time(time)
            if 300 <= time < 86400:
                text = f"Raid mode is currently <code>Disabled</code>\nWould you like to <code>Enable</code> " \
                       f"raid for {readable_time}? "
                keyboard = [
                    [
                        InlineKeyboardButton(
                            "Enable Raid",
                            callback_data=f"enable_raid={chat.id}={time}",
                        ),
                        InlineKeyboardButton(
                            "Cancel Action", callback_data="cancel_raid=0"
                        ),
                    ]
                ]

                reply_markup = InlineKeyboardMarkup(keyboard)
                msg.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
            else:
                msg.reply_text("You can only set time between 5 minutes and 1 day", parse_mode=ParseMode.HTML)

        else:
            msg.reply_text("Unknown time given, give me something like 5m or 1h", parse_mode=ParseMode.HTML)


@Himawaricallback(pattern="enable_raid=")
@connection_status
@user_admin_no_reply
@loggable
def enable_raid_cb(update: Update, ctx: CallbackContext) -> Optional[str]:
    args = update.callback_query.data.replace("enable_raid=", "").split("=")
    chat = update.effective_chat
    user = update.effective_user
    chat_id = args[0]
    time = int(args[1])
    readable_time = get_readable_time(time)
    _, t, acttime = sql.getRaidStatus(chat_id)
    sql.setRaidStatus(chat_id, True, time, acttime)
    update.effective_message.edit_text(f"Raid mode has been <code>Enabled</code> for {readable_time}.",
                                       parse_mode=ParseMode.HTML)
    LOGGER.info("enabled raid mode in {} for {}".format(chat_id, readable_time))
    try:
        oldRaid = RUNNING_RAIDS.pop(int(chat_id))
        j.scheduler.remove_job(oldRaid)  # check if there was an old job
    except KeyError:
        pass

    def disable_raid(_):
        sql.setRaidStatus(chat_id, False, t, acttime)
        LOGGER.info("disbled raid mode in {}".format(chat_id))
        ctx.bot.send_message(chat_id, "Raid mode has been automatically disabled!")

    raid = j.run_once(disable_raid, time)
    RUNNING_RAIDS[int(chat_id)] = raid.job.id
    return (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#RAID\n"
        f"Enabled for {readable_time}\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
    )


@Himawaricallback(pattern="disable_raid=")
@connection_status
@user_admin_no_reply
@loggable
def disable_raid_cb(update: Update, _: CallbackContext) -> Optional[str]:
    args = update.callback_query.data.replace("disable_raid=", "").split("=")
    chat = update.effective_chat
    user = update.effective_user
    chat_id = args[0]
    time = args[1]
    _, _, acttime = sql.getRaidStatus(chat_id)
    sql.setRaidStatus(chat_id, False, time, acttime)
    j.scheduler.remove_job(RUNNING_RAIDS.pop(int(chat_id)))
    update.effective_message.edit_text(
        'Raid mode has been <code>Disabled</code>, newly joining members will no longer be kicked.',
        parse_mode=ParseMode.HTML,
    )
    logmsg = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#RAID\n"
        f"Disabled\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
    )
    return logmsg


@Himawaricallback(pattern="cancel_raid=")
@connection_status
@user_admin_no_reply
def disable_raid_cb(update: Update, _: CallbackContext):
    args = update.callback_query.data.split("=")
    what = args[0]
    update.effective_message.edit_text(
        f"Action cancelled, Raid mode will stay <code>{'Enabled' if what == 1 else 'Disabled'}</code>.",
        parse_mode=ParseMode.HTML)


@Himawaricmd(command="raidtime")
@connection_status
@loggable
@user_admin(AdminPerms.CAN_CHANGE_INFO)
def raidtime(update: Update, context: CallbackContext) -> Optional[str]:
    what, time, acttime = sql.getRaidStatus(update.effective_chat.id)
    args = context.args
    msg = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    if not args:
        msg.reply_text(
            f"Raid mode is currently set to {get_readable_time(time)}\nWhen toggled, the raid mode will last "
            f"for {get_readable_time(time)} then turn off automatically",
            parse_mode=ParseMode.HTML)
        return
    args_time = args[0].lower()
    if time := get_time(args_time):
        readable_time = get_readable_time(time)
        if 300 <= time < 86400:
            text = f"Raid mode is currently set to {readable_time}\nWhen toggled, the raid mode will last for " \
                   f"{readable_time} then turn off automatically"
            msg.reply_text(text, parse_mode=ParseMode.HTML)
            sql.setRaidStatus(chat.id, what, time, acttime)
            return (f"<b>{html.escape(chat.title)}:</b>\n"
                    f"#RAID\n"
                    f"Set Raid mode time to {readable_time}\n"
                    f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n")
        else:
            msg.reply_text("You can only set time between 5 minutes and 1 day", parse_mode=ParseMode.HTML)
    else:
        msg.reply_text("Unknown time given, give me something like 5m or 1h", parse_mode=ParseMode.HTML)


@Himawaricmd(command="raidactiontime", pass_args=True)
@connection_status
@user_admin(AdminPerms.CAN_CHANGE_INFO)
@loggable
def raidtime(update: Update, context: CallbackContext) -> Optional[str]:
    what, t, time = sql.getRaidStatus(update.effective_chat.id)
    args = context.args
    msg = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    if not args:
        msg.reply_text(
            f"Raid action time is currently set to {get_readable_time(time)}\nWhen toggled, the members that "
            f"join will be temp banned for {get_readable_time(time)}",
            parse_mode=ParseMode.HTML)
        return
    args_time = args[0].lower()
    if time := get_time(args_time):
        readable_time = get_readable_time(time)
        if 300 <= time < 86400:
            text = f"Raid action time is currently set to {get_readable_time(time)}\nWhen toggled, the members that" \
                   f" join will be temp banned for {readable_time}"
            msg.reply_text(text, parse_mode=ParseMode.HTML)
            sql.setRaidStatus(chat.id, what, t, time)
            return (f"<b>{html.escape(chat.title)}:</b>\n"
                    f"#RAID\n"
                    f"Set Raid mode action time to {readable_time}\n"
                    f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n")
        else:
            msg.reply_text("You can only set time between 5 minutes and 1 day", parse_mode=ParseMode.HTML)
    else:
        msg.reply_text("Unknown time given, give me something like 5m or 1h", parse_mode=ParseMode.HTML)

__help__ = """

Ever had your group raided by spammers or bots?
This module allows you to quickly stop the raiders
By enabling *raid mode* I will automatically kick every user that tries to join
When the raid is done you can toggle back lockgroup and everything will be back to normal.
  
*Admins only!* 

• /raid `(off/time optional)` : toggle the raid mode (on/off)
if no time is given it will default to 2 hours then turn off automatically
By enabling *raid mode* I will kick every user on joining the group.

• /raidtime `(time optional)` : view or set the default duration for raid mode, after that time from toggling the raid mode will turn off automatically
Default is 6 hours

• /raidactiontime `(time optional)` : view or set the default duration that the raid mode will tempban
Default is 1 hour

"""

__mod_name__ = "AntiRaid"
