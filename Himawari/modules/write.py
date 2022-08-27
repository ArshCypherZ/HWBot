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

import requests
from requests import get

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Himawari import pgram, dispatcher, SUPPORT_CHAT


@pgram.on_message(filters.command("write"))
async def handwrite(_, message: Message):
    if not message.reply_to_message:
        name = (
            message.text.split(None, 1)[1]
            if len(message.command) < 3
            else message.text.split(None, 1)[1].replace(" ", "%20")
        )
        m = await pgram.send_message(
            message.chat.id, "waito..."
        )
        photo = "https://apis.xditya.me/write?text=" + name
        await pgram.send_photo(
            message.chat.id,
            photo=photo
        )
        await m.delete()
    else:
        lol = message.reply_to_message.text
        name = lol.split(None, 0)[0].replace(" ", "%20")
        m = await pgram.send_message(
            message.chat.id, "waito.."
        )
        photo = "https://apis.xditya.me/write?text=" + name
        await pgram.send_photo(
            message.chat.id,
            photo=photo
        )
        await m.delete()


__mod_name__ = "Hand Write"

__help__ = """

Writes the given text on white page with a pen 🖊

/write <text> *:* Writes the given text.
 """