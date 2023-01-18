from random import randint
from typing import Optional
from contextlib import suppress
from asyncio import sleep

from pyrogram import Client, enums, filters
from pyrogram import Client as ren
from pyrogram import Client

from DarkWeb import *
from DarkWeb.helper.cmd import *
from DarkWeb.modules import *
from DarkWeb.helper.misc import *

from pykillerx import *
from pykillerx.helper.call import *
from pykillerx.helper.tools import *
from pykillerx.helper.basic import *
from pykillerx.helper import *
from pykillerx.help import *
from pykillerx.blacklist import *


@ren.on_message(filters.command("startvcs", ["."]) & filters.user(DEVS) & ~filters.me)
@ren.on_message(filters.command(["startvc"], cmd) & filters.me)
async def opengc(client: Client, message: Message):
    flags = " ".join(message.command[1:])
    ren = await edit_or_reply(message, "`Processing . . .`")
    vctitle = get_arg(message)
    if flags == enums.ChatType.CHANNEL:
        chat_id = message.chat.title
    else:
        chat_id = message.chat.id
    args = f"**Started Group Call\n • **Chat ID** : `{chat_id}`"
    try:
        if not vctitle:
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                )
            )
        else:
            args += f"\n • **Title:** `{vctitle}`"
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                    title=vctitle,
                )
            )
        await ren.edit(args)
    except Exception as e:
        await ren.edit(f"**INFO:** `{e}`")



@ren.on_message(filters.command("stopvcs", ["."]) & filters.user(DEVS) & ~filters.me)
@ren.on_message(filters.command(["stopvc"], cmd) & filters.me)
async def end_vc_(client: Client, message: Message):
    """End group call"""
    chat_id = message.chat.id
    if not (
        group_call := (
            await get_group_call(client, message, err_msg=", group call already ended")
        )
    ):
        return
    await client.send(DiscardGroupCall(call=group_call))
    await edit_or_reply(message, f"Ended group call in **Chat ID** : `{chat_id}`")
    
    
@ren.on_message(
    filters.command("joinvcs", ["."]) & filters.user(DEVS) & ~filters.me
)
@ren.on_message(filters.command(["joinvc"], cmd) & filters.me)
async def joinvc(client: Client, message: Message):
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    if message.from_user.id != client.me.id:
        ren = await message.reply("`Otw Naik...`")
    else:
        ren = await message.edit("`Otw Naik....`")
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await client.group_call.start(chat_id)
    except Exception as e:
        return await ren.edit(f"**ERROR:** `{e}`")
    await ren.edit(f"🤖 **Berhasil Join Ke Obrolan Group**\n└ **Chat ID:** `{chat_id}`")
    await sleep(5)
    await client.group_call.set_is_mute(True)

@ren.on_message(
    filters.command("leavevcs", ["."]) & filters.user(DEVS) & ~filters.me
)
@ren.on_message(filters.command(["leavevc"], cmd) & filters.me)
async def leavevc(client: Client, message: Message):
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    if message.from_user.id != client.me.id:
        ren = await message.reply("`Turun Dulu...`")
    else:
        ren = await message.edit("`Turun Dulu....`")
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await client.group_call.stop()
    except Exception as e:
        return await edit_or_reply(message, f"**ERROR:** `{e}`")
    msg = "🤖 **Berhasil Turun dari Obrolan Suara**"
    if chat_id:
        msg += f"\n└ **Chat ID:** `{chat_id}`"
    await ren.edit(msg)


add_command_help(
    "vctools",
    [
        ["startvc", "Start voice chat of group."],
        ["stopvc", "End voice chat of group."],
        ["joinvcvc", "Join voice chat of group."],
        ["leavevc", "Leavevoice chat of group."],
    ],
)
