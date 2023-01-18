import asyncio
from io import BytesIO

from pyrogram import *
from pyrogram.types import *
from pyrogram import Client as ren
from pyrogram import Client

from DarkWeb.helper.cmd import *
from DarkWeb import *
from DarkWeb.helper.misc import *

from pykillerx import *
from pykillerx.helper.basic import *
from pykillerx.helper.hacking import *
from pykillerx.helper.tools import*
from pykillerx.helper import *
from pykillerx.help import *


@ren.on_message(filters.command("carbon", cmd) & filters.me)
async def carbon_func(client: Client, message: Message):
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await message.delete()
    ren = await edit_or_reply(message, "`Preparing Carbon . . .`")
    carbon = await make_carbon(text)
    await ren.edit("`Uploading . . .`")
    await asyncio.gather(
        ren.delete(),
        client.send_photo(
            message.chat.id,
            carbon,
            caption=f"**Carbonised by** {client.me.mention}",
            reply_to_message_id=ReplyCheck(message),
        ),
    )
    carbon.close()


add_command_help(
    "carbon",
    [
        ["carbon <reply>", "carbonisasi text with default settings."],
    ],
)
