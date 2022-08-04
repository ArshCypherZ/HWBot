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

from Himawari import SUPPORT_CHAT
from Himawari.events import register

@register(pattern="[/!]dare")
async def _(rj):
    try:
        resp = requests.get(
            "https://api.truthordarebot.xyz/v1/dare").json()
        results = f"{resp['question']}"
        return await rj.reply(results)
    except Exception:
        await rj.reply(f"Error Report @{SUPPORT_CHAT}")
  

  
@register(pattern="[/!]truth")
async def _(rj):
    try:
        resp = requests.get(
            "https://api.truthordarebot.xyz/v1/truth").json()
        results = f"{resp['question']}"
        return await rj.reply(results)
    except Exception:
        await rj.reply(f"Error Report @{SUPPORT_CHAT}")
