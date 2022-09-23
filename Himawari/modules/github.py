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
from Himawari import dispatcher
from Himawari.modules.disable import DisableAbleCommandHandler
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, run_async

def github(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    args = message.text.split(" ", 1)
    
    if len(args) == 1:
        message.reply_text('Provide me Username, Ex - /github ArshCypherZ')
        return
    else:
        pass
    username = args[1]
    URL = f'https://api.github.com/users/{username}'
    with requests.get(URL) as request:
            if request.status_code == 404:
                return message.reply_text("404")

            result = request.json()
            try:
                url = result['html_url']
                name = result['name']
                company = result['company']
                bio = result['bio']
                created_at = result['created_at']
                avatar_url = result['avatar_url']
                blog = result['blog']
                location = result['location']
                repositories = result['public_repos']
                followers = result['followers']
                following = result['following']
                caption = f"""**Info Of {name}**
**Username:** `{username}`
**Bio:** `{bio}`
**Profile Link:** [Here]({url})
**Company:** `{company}`
**Created On:** `{created_at}`
**Repositories:** `{repositories}`
**Blog:** `{blog}`
**Location:** `{location}`
**Followers:** `{followers}`
**Following:** `{following}`"""
            except Exception as e:
                print(str(e))
                pass
    message.reply_photo(photo=avatar_url, caption=caption, parse_mode=ParseMode.MARKDOWN)


GIT_HANDLER = DisableAbleCommandHandler("github", github, run_async=True)
dispatcher.add_handler(GIT_HANDLER)