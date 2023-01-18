import asyncio

import asyncio
from pyrogram.types import *
from pyrogram.errors import *
from pyrogram import *
from pyrogram import Client as ren
from pyrogram import Client

from DarkWeb.helper.cmd import *
from DarkWeb.helper.misc import *
from DarkWeb.modules.randydev.profile import *

from pykillerx import *
from pykillerx.helper.basic import *
from pykillerx.helper.hacking import *
from pykillerx.helper import *
from pykillerx.help import *

@ren.on_message(filters.command(["sg", "sa", "sangmata"], cmd) & filters.me)
async def sg(client: Client, message: Message):
    args = await extract_user(message)
    lol = await message.edit_text("`Processing...`")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            return await lol.edit(f"`Please specify a valid user!`")
    bot = "SangMataInfo_bot"
    try:
        await client.send_message(bot, f"/search_id {user.id}")
    except YouBlockedUser:
        await client.unblock_user(bot)
        await client.send_message(bot, f"/search_id {user.id}")
    await asyncio.sleep(1)

    async for stalk in client.search_messages(bot, query="Name", limit=1):
        if not stalk:
            await message.edit_text("**Orang Ini Belum Pernah Mengganti Namanya**")
            return
        elif stalk:
            await message.edit(stalk.text)
            await stalk.delete()

    async for stalk in client.search_messages(bot, query="Username", limit=1):
        if not stalk:
            return
        elif stalk:
            await message.reply(stalk.text)
            await stalk.delete()


# testing code by @xtsea

@ren.on_message(filters.command("sgs", cmd) & filters.me)
async def sg2(client: Client, message: Message):
    lol = await message.edit("`Prossing...`")
    args2 = await extract_user(message)
    try:
       user2 = await client.get_users(args2)
    except BaseException:
        pass
    bot2 = "SangMataInfo_bot"
    if args2:
        try:
           await asyncio.sleep(2)
           await lol.delete()
           a = await client.send_message(bot2, f"/search_id {user2.id}")
           await asyncio.sleep(3)
           await a.delete()
        except YouBlockedUser:
            await client.unblock_user(bot2)
            b = await client.send_message(bot2, f"/search_id {user2.id}")
            await asyncio.sleep(2)
            await b.delete()
    async for i in client.get_chat_history(bot2, 3):
        await i.copy(message.chat.id)
        await i.delete()
        try:
           async for f in client.search_messages(message.chat.id, query="Note"):
               await f.delete()
        except BaseException:
            pass

add_command_help(
    "sangmata",
    [
        [f"sg [reply/userid/username]", "Its help uh to find someone name history."],
        [f"sgs userid", "check sangmata."],
    ],
)
