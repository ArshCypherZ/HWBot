from asyncio import gather
from io import BytesIO

from pyrogram.types import Message
from pyrogram import filters

from Himawari import pgram, aiohttpsession as aiosession
from Himawari.utils.errors import capture_err

async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


@pgram.on_message(filters.command("carbon"))
@capture_err
async def carbon_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text("`Reply to a text to generate carbon`")
    if not message.reply_to_message.text:
        return await message.reply_text("`Reply to a text to generate carbon`")
    m = await message.reply_text("`Generating Carbon...`")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("`waitoo...`")
    await pgram.send_photo(message.chat.id, carbon)
    await m.delete()
    carbon.close()


__mod_name__ = "Carbon"

__help__ = """

/carbon *:* Makes carbon for replied text

 """