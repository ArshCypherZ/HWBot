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

from Himawari.modules.disable import DisableAbleCommandHandler
import contextlib
import html
import time
from io import BytesIO
from telegram import Chat, Update, MessageEntity, ParseMode, User
from telegram.error import BadRequest
from telegram.ext import Filters, CallbackContext
from telegram.utils.helpers import mention_html, escape_markdown
from subprocess import Popen, PIPE
from Himawari import DRAGONS as SUDO_USERS
from Himawari import DEMONS as SUPPORT_USERS
from Himawari import WOLVES as WHITELIST_USERS  
from Himawari import (
    dispatcher,
    OWNER_ID,
    DEV_USERS,
    TIGERS,
    INFOPIC,
    sw,
    StartTime
)
from Himawari.__main__ import STATS, USER_INFO
from Himawari.modules.helper_funcs.chat_status import user_admin, sudo_plus
from Himawari.modules.helper_funcs.extraction import extract_user
import Himawari.modules.sql.users_sql as sql
from Himawari.modules.users import __user_info__ as chat_count
from telegram import __version__ as ptbver
from psutil import cpu_percent, virtual_memory, disk_usage, boot_time
import datetime
import platform
from platform import python_version
from Himawari.modules.helper_funcs.decorators import Himawaricmd

MARKDOWN_HELP = f"""
Markdown is a very powerful formatting tool supported by telegram. {dispatcher.bot.first_name} has some enhancements, to make sure that \
saved messages are correctly parsed, and to allow you to create buttons.

- <code>_italic_</code>: wrapping text with '_' will produce italic text
- <code>*bold*</code>: wrapping text with '*' will produce bold text
- <code>`code`</code>: wrapping text with '`' will produce monospaced text, also known as 'code'
- <code>[sometext](someURL)</code>: this will create a link - the message will just show <code>sometext</code>, \
and tapping on it will open the page at <code>someURL</code>.
EG: <code>[test](example.com)</code>

- <code>[buttontext](buttonurl:someURL)</code>: this is a special enhancement to allow users to have telegram \
buttons in their markdown. <code>buttontext</code> will be what is displayed on the button, and <code>someurl</code> \
will be the url which is opened.
EG: <code>[This is a button](buttonurl:example.com)</code>

If you want multiple buttons on the same line, use :same, as such:
<code>[one](buttonurl://example.com)
[two](buttonurl://google.com:same)</code>
This will create two buttons on a single line, instead of one button per line.

Keep in mind that your message <b>MUST</b> contain some text other than just a button!
"""


@Himawaricmd(command='gifid')
def gifid(update: Update, _):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.animation:
        update.effective_message.reply_text(
            f"Gif ID:\n<code>{msg.reply_to_message.animation.file_id}</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text("Please reply to a gif to get its ID.")

@Himawaricmd(command='info', pass_args=True)
def info(update: Update, context: CallbackContext):  # sourcery no-metrics
    bot = context.bot
    args = context.args
    message = update.effective_message
    chat = update.effective_chat
    if user_id := extract_user(update.effective_message, args):
        user = bot.get_chat(user_id)

    elif not message.reply_to_message and not args:
        user = (
            message.sender_chat
            if message.sender_chat is not None
            else message.from_user
        )

    elif not message.reply_to_message and (
        not args
        or (
            len(args) >= 1
            and not args[0].startswith("@")
            and not args[0].lstrip("-").isdigit()
            and not message.parse_entities([MessageEntity.TEXT_MENTION])
        )
    ):
        message.reply_text("I can't extract a user from this.")
        return

    else:
        return

    if hasattr(user, 'type') and user.type != "private":
        text = get_chat_info(user)
        is_chat = True
    else:
        text = get_user_info(chat, user)
        is_chat = False

    if INFOPIC:
        if is_chat:
            try:
                pic = user.photo.big_file_id
                pfp = bot.get_file(pic).download(out=BytesIO())
                pfp.seek(0)
                message.reply_document(
                        document=pfp,
                        filename=f'{user.id}.jpg',
                        caption=text,
                        parse_mode=ParseMode.HTML,
                )
            except AttributeError:  # AttributeError means no chat pic so just send text
                message.reply_text(
                        text,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                )
        else:
            try:
                profile = bot.get_user_profile_photos(user.id).photos[0][-1]
                _file = bot.get_file(profile["file_id"])

                _file = _file.download(out=BytesIO())
                _file.seek(0)

                message.reply_document(
                        document=_file,
                        caption=(text),
                        parse_mode=ParseMode.HTML,
                )

            # Incase user don't have profile pic, send normal text
            except IndexError:
                message.reply_text(
                        text, parse_mode=ParseMode.HTML, disable_web_page_preview=True
                )

    else:
        message.reply_text(
            text, parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )


def get_user_info(chat: Chat, user: User) -> str:
    bot = dispatcher.bot
    text = (
        f"╒═══「<b> Analyzed Results:</b> 」\n"
        f"User ID: <code>{user.id}</code>\n"
        f"⫸ First Name: {html.escape(user.first_name)}"
    )
    if user.last_name:
        text += f"\n⫸ Last Name: {html.escape(user.last_name)}"
    if user.username:
        text += f"\n⫸ Username: @{html.escape(user.username)}"
    text += f"\n⫸ User link: {mention_html(user.id, 'link')}"
    with contextlib.suppress(Exception):
        if spamwtc := sw.get_ban(int(user.id)):
            text += "<b>\n\nSpamWatch:\n</b>"
            text += "<b>This person is banned in Spamwatch!</b>"
            text += f"\nReason: <pre>{spamwtc.reason}</pre>"
            text += "\nAppeal at @SpamWatchSupport"
        else:
            text += "<b>\n\nSpamWatch:</b> Not banned"
    disaster_level_present = False
    num_chats = sql.get_user_num_chats(user.id)
    text += f"\n\n<b>Chat count</b>: <code>{num_chats}</code>"
    with contextlib.suppress(BadRequest):
        user_member = chat.get_member(user.id)
        if user_member.status == "administrator":
            result = bot.get_chat_member(chat.id, user.id)
            if result.custom_title:
                text += f"\n\nThis user holds the title <b>{result.custom_title}</b> here."
    if user.id == OWNER_ID:        
        text += "\n\n<code>Our Cute Neko Arsh</code> :3"
        disaster_level_present = True
    elif user.id in DEV_USERS:
        text += "\n\n<code>This user is a part of our family</code> 🌻"
        disaster_level_present = True
    elif user.id in SUDO_USERS:
        text += "\n\n<code>One of our besto friendos, touch him and you are dead meat</code>"
        disaster_level_present = True
    elif user.id in SUPPORT_USERS:
        text += "\n\n<code>This user is our friend</code> ✨"
        disaster_level_present = True
    elif user.id in TIGERS:
        text += "\n\n<code>One of my classmates</code> :p"
        disaster_level_present = True
    elif user.id in WHITELIST_USERS:
        text += "\n\n<code>Member of Himawari Tech, totally cool right?</code>"
        disaster_level_present = True
    if disaster_level_present:
        text += ' [<a href="https://t.me/IgniteTechUpdates/13">?</a>]'
    text += "\n"
    for mod in USER_INFO:
        if mod.__mod_name__ == "Users":
            continue

        try:
            mod_info = mod.__user_info__(user.id)
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id)
        if mod_info:
            text += "\n" + mod_info
    return text


def get_chat_info(user):
    text = (
        f"<b>Chat Information:</b>\n"
        f"<b>Chat Title:</b> {user.title}"
    )
    if user.username:
        text += f"\n<b>Username:</b> @{html.escape(user.username)}"
    text += f"\n<b>Chat ID:</b> <code>{user.id}</code>"
    text += f"\n<b>Chat Type:</b> {user.type.capitalize()}"
    text += "\n" + chat_count(user.id)

    return text


def shell(command):
    process = Popen(command, stdout=PIPE, shell=True, stderr=PIPE)
    stdout, stderr = process.communicate()
    return (stdout, stderr)

@Himawaricmd(command='markdownhelp', filters=Filters.chat_type.private)
def markdown_help(update: Update, _):
    chat = update.effective_chat
    update.effective_message.reply_text(f"{MARKDOWN_HELP}", parse_mode=ParseMode.HTML)
    update.effective_message.reply_text(
        "Try forwarding the following message to me, and you'll see!"
    )
    update.effective_message.reply_text(
        "/save test This is a markdown test. _italics_, *bold*, `code`, "
        "[URL](example.com) [button](buttonurl:github.com) "
        "[button2](buttonurl://google.com:same)"
    )

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += f'{time_list.pop()}, '

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

stats_str = '''
'''
@Himawaricmd(command='stats', can_disable=False)
@sudo_plus
def stats(update, context):
    uptime = datetime.datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    botuptime = get_readable_time((time.time() - StartTime))
    status = "*╒═══「 System statistics: 」*\n\n"
    status += f"*• System Start time:* {str(uptime)}" + "\n"
    uname = platform.uname()
    status += f"*• System:* {str(uname.system)}" + "\n"
    status += f"*• Node name:* {escape_markdown(str(uname.node))}" + "\n"
    status += f"*• Release:* {escape_markdown(str(uname.release))}" + "\n"
    status += f"*• Machine:* {escape_markdown(str(uname.machine))}" + "\n"

    mem = virtual_memory()
    cpu = cpu_percent()
    disk = disk_usage("/")
    status += f"*• CPU:* {str(cpu)}" + " %\n"
    status += f"*• RAM:* {str(mem[2])}" + " %\n"
    status += f"*• Storage:* {str(disk[3])}" + " %\n\n"
    status += f"*• Python version:* {python_version()}" + "\n"
    status += f"*• python-telegram-bot:* {str(ptbver)}" + "\n"
    status += f"*• Uptime:* {str(botuptime)}" + "\n"

    try:
        update.effective_message.reply_text(status +
            "\n*Bot statistics*:\n"
            + "\n".join([mod.__stats__() for mod in STATS]) +
            "\n\n[⍙ GitHub](https://github.com/ArshCypherZ/HWBot) | [Telegram](https://t.me/Himawari_robot)\n\n" +
            "╘══「 by [Vicious Alliance](t.me/ViciousAlliance) 」\n",
        parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    except BaseException:
        update.effective_message.reply_text(
            (
                (
                    (
                        "\n*Bot statistics*:\n"
                        + "\n".join(mod.__stats__() for mod in STATS)
                    )
                    + "\n\n⍙ [GitHub](https://github.com/ArshCypherZ/HWBot) | [Telegram](https://t.me/Himawari_Robot)\n\n"
                )
                + "╘══「 by [Vicious Alliance](t.me/ViciousAlliance) 」\n"
            ),
            parse_mode=ParseMode.MARKDOWN,         
            disable_web_page_preview=True,
        )




@user_admin
def echo(update: Update, context: CallbackContext):
    args = update.effective_message.text.split(None, 1)
    message = update.effective_message

    if message.reply_to_message:
        message.reply_to_message.reply_text(
            args[1], parse_mode="MARKDOWN", disable_web_page_preview=True,
        )
    else:
        message.reply_text(
            args[1], quote=False, parse_mode="MARKDOWN", disable_web_page_preview=True,
        )
    message.delete()    


__help__ = """
*Available commands:*

📐 Markdown:

• `/markdownhelp`: quick summary of how markdown works in telegram - can only be called in private chats


🗳  Other Commands:

Paste:
• `/paste`*:* Saves replied content to nekobin.com and replies with a url

React:
• `/react`*:* Reacts with a random reaction

Urban Dictonary:
• `/ud <word>`*:* Type the word or expression you want to search use

Wikipedia:
• `/wiki <query>`*:* wikipedia your query

Wallpapers:
• `/wall <query>`*:* get a wallpaper from alphacoders

Books:
• `/book <book name>`*:* Gets Instant Download Link Of Given Book.

"""

ECHO_HANDLER = DisableAbleCommandHandler("echo", echo, filters=Filters.chat_type.groups, run_async=True)

dispatcher.add_handler(ECHO_HANDLER)

__mod_name__ = "Extras"
__command_list__ = ["id", "echo"]
__handlers__ = [
    ECHO_HANDLER
]
