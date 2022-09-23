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
from telethon import events
from Himawari import telethn as meow

@meow.on(events.NewMessage(pattern="^/cosplay"))
async def waifu(event):
  r = requests.get("https://waifu-api.vercel.app").json() #api credit- @YASH_SHARMA_1807 on telegram
  await event.reply(file=r)
  
@meow.on(events.NewMessage(pattern="^/lewd"))
async def waifu(event):
  r = requests.get("https://waifu-api.vercel.app/items/1").json()
  await event.reply(file=r)

__mod_name__ = "Cosplay"
__help__ = """
Just a weeb type module to get anime cosplay and lewd pictures
- /cosplay
- /lewd
"""