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
# if kanging please do not remove credits else i will turn off my api :) ~
# ArshCypherZ


import asyncio
import random

from requests import get

from Himawari import telethn as meow
from Himawari.events import register


@register(pattern="^[!/]wall")
async def some(event):
    try:
        inpt: str = (
            event.text.split(None, 1)[1]
            if len(event.text) < 3
            else event.text.split(None, 1)[1].replace(" ", "%20")
        )
    except IndexError:
        return await event.reply("Usage: /wall <query>")

    Emievent = await event.reply("Sending please wait...")
    try:
        r = get(
            f"https://bakufuapi.vercel.app/api/wall/wallhaven?query={inpt}&page=1"
        ).json()

        list_id = [r["response"][i]["path"] for i in range(len(r["response"]))]
        item = (random.sample(list_id, 1))[0]
    except BaseException:
        await Emievent.delete()
        return await event.reply("Try again later or enter correct query.")

    await meow.send_file(event.chat_id, item, caption="Preview", reply_to=event)
    await meow.send_file(
        event.chat_id, file=item, caption="wall", reply_to=event, force_document=True
    )
    await Emievent.delete()
    await asyncio.sleep(5)
