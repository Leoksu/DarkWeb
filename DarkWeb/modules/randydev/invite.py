import asyncio
from pyrogram import *
from pyrogram import Client as ren
from pyrogram import Client
from pyrogram.enums import *
from pyrogram.types import *
from pyrogram.errors.exceptions.flood_420 import *

from DarkWeb import *
from DarkWeb.helper.cmd import *

from pykillerx import *
from pykillerx.helper import *
from pykillerx.help import *


@ren.on_message(filters.command(["invite"], cmd) & filters.me)
async def inviteee(client: Client, message: Message):
    mg = await message.reply_text("`Adding Users!`")
    user_s_to_add = message.text.split(" ", 1)[1]
    if not user_s_to_add:
        await mg.edit("`Give Me Users To Add! Check Help Menu For More Info!`")
        return
    user_list = user_s_to_add.split(" ")
    try:
        await client.add_chat_members(message.chat.id, user_list, forward_limit=100)
    except BaseException as e:
        await mg.edit(f"`Unable To Add Users! \nTraceBack : {e}`")
        return
    await mg.edit(f"`Sucessfully Added {len(user_list)} To This Group / Channel!`")

@ren.on_message(
    filters.command(["inviteall"], cmd) & filters.me)
async def inv(client: Client, message: Message):
    ex = await message.reply_text("`Processing . . .`")
    text = message.text.split(" ", 1)
    queryy = text[1]
    chat = await client.get_chat(queryy)
    tgchat = message.chat
    await ex.edit_text(f"inviting users from {chat.username}")
    async for member in client.get_chat_members(chat.id):
        user = member.user
        zxb = [
            UserStatus.ONLINE,
            UserStatus.OFFLINE,
            UserStatus.RECENTLY,
            UserStatus.LAST_WEEK,
        ]
        if user.status in zxb:
            try:
                await client.add_chat_members(tgchat.id, user.id)
            except FloodWait as e:
                return
            except Exception as e:
                pass

@ren.on_message(filters.command("invitelink", cmd) & filters.me)
async def invite_link(client: Client, message: Message):
    um = await message.edit_text("`Processing...`")
    if message.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        message.chat.title
        try:
            link = await client.export_chat_invite_link(message.chat.id)
            await um.edit(f"**Link Invite:** {link}")
        except Exception:
            await um.edit("Denied permission")


add_command_help(
    "scraper",
    [
        ["invitelink", "Get your private invite link. [Need Admin]"],
        ["invite @username", "to invite someone."],
        ["inviteall @username", "Mass adding (can affect your account)."],
    ],
)
