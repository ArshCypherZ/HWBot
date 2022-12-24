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

from Himawari.events import register
from io import BytesIO
from requests import get
from telethon import events

@register(pattern="^/write")
async def writer(m: events.NewMessage):
    if not m.reply_to_msg_id:
        text: str = (
            m.text.split(None, 1)[1]
            if len(m.text) < 3
            else m.text.split(None, 1)[1].replace(" ", "%20")
        )
    else:
        reply: str = (await m.get_reply_message()).text
        text = reply.split(" ")[1].replace(" ", "%20")

    var: str = await m.reply("`Waitoo...`")
    with BytesIO(get(f"https://apis.xditya.me/write?text={text}").content) as file:
        file.name: str = "image.jpg"
        await m.reply(file=file)
    await var.delete()


__mod_name__ = "Hand Write"

__help__ = """
Writes the given text on white page with a pen 🖊

/write <text> *:* Writes the given text.
 """