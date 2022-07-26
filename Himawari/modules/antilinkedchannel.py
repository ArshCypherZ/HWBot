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

from telegram import Update, TelegramError
from telegram.ext import CallbackContext
from telegram.ext.filters import Filters
from Himawari.modules.helper_funcs.chat_status import bot_admin, bot_can_delete

from Himawari.modules.helper_funcs.decorators import Himawaricmd, Himawarimsg
from Himawari.modules.helper_funcs.anonymous import user_admin, AdminPerms
import Himawari.modules.sql.antilinkedchannel_sql as sql


@Himawaricmd(command="cleanlinked", group=112)
@bot_can_delete
@user_admin(AdminPerms.CAN_RESTRICT_MEMBERS)
def set_antilinkedchannel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) > 0:
        s = args[0].lower()
        if s in ["yes", "on"]:
            if sql.status_pin(chat.id):
                sql.disable_pin(chat.id)
                sql.enable_pin(chat.id)
                message.reply_html(
                    f"Enabled Linked channel post deletion and Disabled anti channel pin in {html.escape(chat.title)}"
                )

            else:
                sql.enable_linked(chat.id)
                message.reply_html(
                    f"Enabled linked channel post deletion in {html.escape(chat.title)}. Messages sent from the linked channel will be deleted."
                )

        elif s in ["off", "no"]:
            sql.disable_linked(chat.id)
            message.reply_html(
                f"Disabled linked channel post deletion in {html.escape(chat.title)}"
            )

        else:
            message.reply_text(f"Unrecognized arguments {s}")
        return
    message.reply_html(
        f"Linked channel post deletion is currently {sql.status_linked(chat.id)} in {html.escape(chat.title)}"
    )


@Himawarimsg(Filters.is_automatic_forward, group=111)
def eliminate_linked_channel_msg(update: Update, _: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    if not sql.status_linked(chat.id):
        return
    try:
        message.delete()
    except TelegramError:
        return

@Himawaricmd(command="antichannelpin", group=114)
@bot_admin
@user_admin(AdminPerms.CAN_RESTRICT_MEMBERS)
def set_antipinchannel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    if len(args) > 0:
        s = args[0].lower()
        if s in ["yes", "on"]:
            if sql.status_linked(chat.id):
                sql.disable_linked(chat.id)
                sql.enable_pin(chat.id)
                message.reply_html(
                    f"Disabled Linked channel deletion and Enabled anti channel pin in {html.escape(chat.title)}"
                )

            else:
                sql.enable_pin(chat.id)
                message.reply_html(f"Enabled anti channel pin in {html.escape(chat.title)}")
        elif s in ["off", "no"]:
            sql.disable_pin(chat.id)
            message.reply_html(f"Disabled anti channel pin in {html.escape(chat.title)}")
        else:
            message.reply_text(f"Unrecognized arguments {s}")
        return
    message.reply_html(
        f"Linked channel message unpin is currently {sql.status_pin(chat.id)} in {html.escape(chat.title)}"
    )


@Himawarimsg(Filters.is_automatic_forward | Filters.status_update.pinned_message, group=113)
def eliminate_linked_channel_msg(update: Update, _: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    if not sql.status_pin(chat.id):
        return
    try:
        message.unpin()
    except TelegramError:
        return
