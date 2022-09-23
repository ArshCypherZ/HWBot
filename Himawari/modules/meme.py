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
import urllib
import random
import requests

from Himawari import telethn as meow
from requests import get
from telethon import events

import logging

logging.basicConfig(level=logging.DEBUG)

MemesReddit = [
    "Animemes", "lostpause", "LoliMemes", "cleananimemes",
    "animememes", "goodanimemes", "AnimeFunny", "dankmemes",
    "teenagers", "shitposting", "Hornyjail", "wholesomememes",
    "cursedcomments"
]

@meow.on(events.NewMessage(pattern="^/memes"))
async def mimi(event):
    try:
        memereddit = random.choice(MemesReddit)
        meme_link = f"https://meme-api.herokuapp.com/gimme/{memereddit}"
        q = requests.get(meme_link).json()
        await event.reply(q["title"], file=q["url"])
        
    except Exception as e:
        print(e)

@meow.on(events.NewMessage(pattern="^/dank"))
async def mimi(event):
    try:
        memereddit = random.choice(MemesReddit)
        meme_link = "https://meme-api.herokuapp.com/gimme/dankmemes"
        q = requests.get(meme_link).json()
        await event.reply(q["title"], file=q["url"])
        
    except Exception as e:
        print(e) 

@meow.on(events.NewMessage(pattern="^/lolimeme"))
async def mimi(event):
    try:
        memereddit = random.choice(MemesReddit)
        meme_link = "https://meme-api.herokuapp.com/gimme/LoliMemes"
        q = requests.get(meme_link).json()
        await event.reply(q["title"], file=q["url"])
        
    except Exception as e:
        print(e)   

@meow.on(events.NewMessage(pattern="^/hornyjail"))
async def mimi(event):
    try:
        memereddit = random.choice(MemesReddit)
        meme_link = "https://meme-api.herokuapp.com/gimme/Hornyjail"
        q = requests.get(meme_link).json()
        await event.reply(q["title"], file=q["url"])
        
    except Exception as e:
        print(e)

@meow.on(events.NewMessage(pattern="^/wmeme"))
async def mimi(event):
    try:
        memereddit = random.choice(MemesReddit)
        meme_link = "https://meme-api.herokuapp.com/gimme/wholesomememes"
        q = requests.get(meme_link).json()
        await event.reply(q["title"], file=q["url"])
        
    except Exception as e:
        print(e)

@meow.on(events.NewMessage(pattern="^/pewds"))
async def mimi(event):
    try:
        memereddit = random.choice(MemesReddit)
        meme_link = "https://meme-api.herokuapp.com/gimme/PewdiepieSubmissions"
        q = requests.get(meme_link).json()
        await event.reply(q["title"], file=q["url"])
        
    except Exception as e:
        print(e)

@meow.on(events.NewMessage(pattern="^/hmeme"))
async def mimi(event):
    try:
        memereddit = random.choice(MemesReddit)
        meme_link = "https://meme-api.herokuapp.com/gimme/hornyresistance"
        q = requests.get(meme_link).json()
        await event.reply(q["title"], file=q["url"])
        
    except Exception as e:
        print(e)

@meow.on(events.NewMessage(pattern="^/teen"))
async def mimi(event):
    try:
        memereddit = random.choice(MemesReddit)
        meme_link = "https://meme-api.herokuapp.com/gimme/teenagers"
        q = requests.get(meme_link).json()
        await event.reply(q["title"], file=q["url"])
        
    except Exception as e:
        print(e)

@meow.on(events.NewMessage(pattern="^/fbi"))
async def mimi(event):
    try:
        memereddit = random.choice(MemesReddit)
        meme_link = "https://meme-api.herokuapp.com/gimme/FBI_Memes"
        q = requests.get(meme_link).json()
        await event.reply(q["title"], file=q["url"])
        
    except Exception as e:
        print(e)

@meow.on(events.NewMessage(pattern="^/shitposting"))
async def mimi(event):
    try:
        memereddit = random.choice(MemesReddit)
        meme_link = "https://meme-api.herokuapp.com/gimme/shitposting"
        q = requests.get(meme_link).json()
        await event.reply(q["title"], file=q["url"])
        
    except Exception as e:
        print(e)


@meow.on(events.NewMessage(pattern="^/cursed"))
async def mimi(event):
    try:
        memereddit = random.choice(MemesReddit)
        meme_link = "https://meme-api.herokuapp.com/gimme/cursedcomments"
        q = requests.get(meme_link).json()
        await event.reply(q["title"], file=q["url"])
        
    except Exception as e:
        print(e)

__help__ = """
Memes help you get through tough times, enjoy memes with our funny and horny memes

Usage:
- /memes Will give you mixed memes
- /wmeme Will give you wholesome memes
- /dank Provides dank memes
- /cursed Cursed memes
- /shitposting Random shitposts
- /fbi FBI Memes
- /teen Teenagers meme
- /hmeme Horny Memes
- /pewds Pewdiepie Collection
- /hornyjail Onichan Arrested :p
- /lolimeme Loli Memes (**fbi locating**)
"""

__mod_name__ = "Memes"