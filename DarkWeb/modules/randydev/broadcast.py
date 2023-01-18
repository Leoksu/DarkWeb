import asyncio

from pyrogram import Client, enums, filters
from pyrogram import Client as ren
from pyrogram.types import Message
from requests import get

from DarkWeb import *
from DarkWeb.helper.cmd import *
from config import *

from pykillerx import *
from pykillerx.helper import *
from pykillerx.blacklist import *
from pykillerx.help import *

BLACKLIST = GROUP

def get_arg(message: Message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])

@ren.on_message(filters.command(["gcast"], cmd) & filters.me)
async def gcast_cmd(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        tex = await message.reply_text("`Started global broadcast...`")
    else:
        return await message.edit_text("**Give A Message or Reply**")
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            if chat not in BLACKLIST and chat not in GCAST_BLACKLIST:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    elif get_arg:
                        await client.send_message(chat, msg)
                    done += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    error += 1
                    await asyncio.sleep(0.3)
    await tex.edit_text(
        f"**Successfully Sent Message To** `{done}` **Groups, chat, Failed to Send Message To** `{error}` **Groups**"
    )


@ren.on_message(filters.command(["gforward"], cmd) & filters.me)
async def gforward(client: Client, message: Message):
    if message.reply_to_message:
        lol = await message.reply_text("`Started global broadcast forward...`")
    else:
        return await message.edit_text("**Please reply**")
    kntl = 0
    rusak = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            if message.reply_to_message:
                msg = message.reply_to_message
            chat = dialog.chat.id
            if chat not in BLACKLIST and chat not in GCAST_BLACKLIST:
                try:
                    if message.reply_to_message:
                        await msg.forward(chat, disable_notification=True)
                    kntl += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    rusak += 1
                    await asyncio.sleep(0.3)
    await lol.edit_text(
        f"**Successfully Sent Message To** `{kntl}` **Groups Forwarded, Failed to Send Message To** `{rusak}` **Groups**"
    )

@ren.on_message(filters.command(["guforward"], cmd) & filters.me)
async def guforward(client: Client, message: Message):
    if message.reply_to_message:
        lol = await message.reply_text("`Started global broadcast pm private forward...`")
    else:
        return await message.edit_text("**Please reply**")
    kntl = 0
    rusak = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE and not dialog.chat.is_verified:
            if message.reply_to_message:
                msg = message.reply_to_message
            chat = dialog.chat.id
            if chat not in DEVS:
                try:
                    if message.reply_to_message:
                        await msg.forward(chat, disable_notification=True)
                    kntl += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    rusak += 1
                    await asyncio.sleep(0.3)
    await lol.edit_text(
        f"**Successfully Sent Message To** `{kntl}` **pm forward, Failed to Send Message To** `{rusak}` **Chat**"
    )



@ren.on_message(filters.command(["gucast"], cmd) & filters.me)
async def gucast(client: Client, message: Message):
    if message.reply_to_message or get_arg(message):
        tex = await message.reply_text("`Started global broadcast...`")
    else:
        return await message.edit_text("**Give A Message or Reply**")
    done = 0
    error = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE and not dialog.chat.is_verified:
            if message.reply_to_message:
                msg = message.reply_to_message
            elif get_arg:
                msg = get_arg(message)
            chat = dialog.chat.id
            if chat not in DEVS:
                try:
                    if message.reply_to_message:
                        await msg.copy(chat)
                    elif get_arg:
                        await client.send_message(chat, msg)
                    done += 1
                    await asyncio.sleep(0.3)
                except Exception:
                    error += 1
                    await asyncio.sleep(0.3)
    await tex.edit_text(
        f"**Successfully Sent Message To** `{done}` **pm forward, Failed to Send Message To** `{error}` **chat**"
    )


add_command_help(
    "broadcast",
    [
        [f"gcast [text/reply]", "Sending Global Broadcast messages to all groups you are logged into. (Can Send Media/Sticker)"],
        [f"gforward [reply]", "Sending Global Broadcast message to all group forwarded messages"],
        [f"guforward [reply]", "Sending Global Broadcast messages to all incoming Private Massages Forward"],
        [f"gucast [text/reply]", "Sending Global Broadcast messages to all incoming Private Massages / PCs. (Can Send Media/Sticker)"],
    ],
)
