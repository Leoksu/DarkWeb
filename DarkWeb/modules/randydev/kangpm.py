"""
COPYRIGHT 2020 - 2023 https://github.com/TeamKillerX/DarkWeb
CREDITS : https://t.me/xtsea
PLEASE DON'T REMOVE CREDITS
"""

import asyncio
from pyrogram import *
from pyrogram.types import *
from pyrogram import Client as ren
from pyrogram import Client

from DarkWeb.helper.cmd import *
from DarkWeb.helper.misc import *

from pykillerx import *
from pykillerx.helper import *
from pykillerx.helper.basic import *
from pykillerx.helper.hacking import *
from pykillerx.help import *

from config import *

@ren.on_message(filters.command("takepm", cmd) & filters.me)
async def takepm(client: Client, message: Message):
    lol = message.reply_to_message
    if not lol:
       return await message.edit("**Please reply**")
    try:
       await lol.copy(message.from_user.id)
       await message.delete()
    except BaseException:
        pass

@ren.on_message(filters.command("take", cmd) & filters.me)
async def take(client: Client, message: Message):
    lol = message.reply_to_message
    if not lol:
       return await message.edit("**Please reply**")
    try:
       await lol.copy(message.chat.id)
       await message.delete()
    except BaseException:
        pass


@ren.on_message(filters.command("fwd", cmd) & filters.me)
async def fwd(client: Client, message: Message):
    lol = message.reply_to_message
    if not lol:
       return await message.edit("**Please reply**")
    try:
       await lol.forward(message.chat.id)
       await message.delete()
    except BaseException:
        pass

# CREDITS @XTSEA
# JANGAN HAPUS CREDIT // GUA GBAN LO KONTOL
@ren.on_message(filters.command("stealpm", cmd) & filters.me)
async def stealch(client: Client, message: Message):
    tai = await message.reply_text("`Steal channel media.....`")
    kntl = get_arg(message)
    ok = 0
    error = 0
    if kntl:
        try:
           RendyProjects
        except:
            return await message.edit("channel banned 😔")
        try:
           async for mmk in client.search_messages(kntl):
               await mmk.copy(message.from_user.id)
               ok += 1
               await asyncio.sleep(0.3)
        except Exception:
            error += 1
            await asyncio.sleep(0.3)
    await tai.edit_text(f"**Successfully Steal channel** `{ok}` **Failed** `{error}`")

@ren.on_message(filters.command("cp", cmd) & filters.me)
async def cp(client: Client, message: Message):
    tulis = get_arg(message)
    user = message.reply_to_message
    if not tulis and not user:
       return await message.edit("lu goblok") 
    try:
       await user.copy(message.chat.id, caption=tulis)
    except Exception as e:
        return await message.edit(f"**ERROR** `{e}`")

add_command_help(
    "kangpm",
    [
        [f"takepm [reply]", "saved messages."],
        [f"take [reply]", "I take another."],
        [f"fwd [reply]", "forward messages from the group."],
        [f"stealpm [username]", "without username @ example : `stealch durov`."],
        [f"cp [photo/caption]", "I copied the photo so that it was written."],
    ],
)
