
import html

from telegram import ParseMode
from telegram import (InlineKeyboardButton,
                      InlineKeyboardMarkup, ParseMode, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler)
from telegram.utils.helpers import mention_html
from Himawari import  dispatcher
from Himawari.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply


from Himawari import MONGO_DB_URL

from pymongo import MongoClient

worddb = MongoClient(MONGO_DB_URL) 
k = worddb["Himalol"]["karma_toggle"]
 

@user_admin_no_reply
def karmarem(update: Update, context:CallbackContext):
    query= update.callback_query
    bot = context.bot
    user = update.effective_user
    if query.data == "rem_karma":
        chat = update.effective_chat
        done = k.insert_one({"chat_id": chat.id})    
        update.effective_message.edit_text(
            f"{dispatcher.bot.first_name} Karma System Disabled by {mention_html(user.id, user.first_name)}.",
            parse_mode=ParseMode.HTML,
        )
               


@user_admin_no_reply
def karmaadd(update: Update, context:CallbackContext):
    query= update.callback_query
    bot = context.bot
    user = update.effective_user
    if query.data == "add_karma":
        chat = update.effective_chat
        done = k.delete_one({"chat_id": chat.id})            
        update.effective_message.edit_text(
            f"{dispatcher.bot.first_name} Karma System Enabled by {mention_html(user.id, user.first_name)}.",
            parse_mode=ParseMode.HTML,
        )           

@user_admin
@loggable
def karmacmd(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    is_chatbot = k.find_one({"chat_id": chat.id})
    if is_chatbot:
        msg = "Karma Toggle\n Mode : DISABLE"
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                text="Enable",
                callback_data=r"add_karma")]])     
        message.reply_text(
            msg,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
        )
    if not is_chatbot:
        msg = "Karma Toggle\n Mode : ENABLE"
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                text="Disable",
                callback_data=r"rem_karma")]])     
        message.reply_text(
            msg,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
        )

KARMA_CMD_HANDLER = CommandHandler("karma", karmacmd, run_async = True)
ADD_KARMA_HANDLER = CallbackQueryHandler(karmaadd, pattern=r"add_karma", run_async = True)
REM_KARMA_HANDLER = CallbackQueryHandler(karmarem, pattern=r"rem_karma", run_async = True)

dispatcher.add_handler(KARMA_CMD_HANDLER)
dispatcher.add_handler(ADD_KARMA_HANDLER)
dispatcher.add_handler(REM_KARMA_HANDLER)

__handlers__ = [
    KARMA_CMD_HANDLER,
    ADD_KARMA_HANDLER,
    REM_KARMA_HANDLER,
]
