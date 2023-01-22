"""
COPYRIGHT 2020 - 2023 : https://github.com/TeamKillerX/DarkWeb
CREDITS DEVELOPER BY : @XTSEA
"""

from pyrogram import *
from pyrogram.types import *
from pyrogram import Client as ren

from DarkWeb.helper.cmd import *
from DarkWeb.helper.misc import *

from pykillerx import *
from pykillerx.helper import *
from pykillerx.helper.basic import *
from pykillerx.helper.hacking import *
from pykillerx.help import *

@ren.on_message(filters.command("tagm", cmd) & filters.me)
async def tagm(client: Client, message: Message):
    tag = get_arg(message)
    args = await extract_user(message)
    lol = message.reply_to_message
    if not args and not lol:
       return await message.edit("**Please Reply**")
    if tag:
       try:
          await lol.reply_text(f"<a href=tg://user?id={lol.from_user.id}>{tag}</a>")
          await message.delete()
       except Exception as e:
           return await message.edit(f"**ERROR** `{e}`")
