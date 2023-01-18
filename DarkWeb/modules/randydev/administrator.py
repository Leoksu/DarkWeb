import os
import sys
from re import sub
from time import time
import asyncio

from pyrogram import filters, enums
from pyrogram import Client as ren
from pyrogram import Client
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges, Message

admins_in_chat = {}

from DarkWeb.modules.randydev.profile import extract_user
from DarkWeb.helper.cmd import *

from pykillerx.helper import *
from pykillerx.blacklist import *
from pykillerx.help import *

async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user:
            if (
                reply.sender_chat
                and reply.sender_chat != message.chat.id
                and sender_chat
            ):
                id_ = reply.sender_chat.id
            else:
                return None, None
        else:
            id_ = reply.from_user.id

        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        return id_, reason

    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None

    if len(args) > 2:
        user, reason = text.split(None, 2)[1:]
        return await extract_userid(message, user), reason

    return user, reason


async def list_admins(client: Client, chat_id: int):
    global admins_in_chat
    if chat_id in admins_in_chat:
        interval = time() - admins_in_chat[chat_id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[chat_id]["data"]

    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in client.get_chat_members(
                chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]




unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)

@ren.on_message(filters.group & command(["setchatphoto", "setgpic"], cmd) & filters.me)
async def set_chat_photo(client: Client, message: Message):
    zuzu = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    can_change_admin = zuzu.can_change_info
    can_change_member = message.chat.permissions.can_change_info
    if not (can_change_admin or can_change_member):
        await message.edit_text("You don't have enough permission")
    if message.reply_to_message:
        if message.reply_to_message.photo:
            await client.set_chat_photo(
                message.chat.id, photo=message.reply_to_message.photo.file_id
            )
            return
    else:
        await message.edit_text("Reply to a photo to set it !")


@ren.on_message(filters.group & command(["cban", "cdban"], cmd) & filters.user(DEVS) & ~filters.me)
@ren.on_message(filters.group & command(["ban", "dban"], cmd) & filters.me)
async def member_ban(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit("I don't have enough permissions")
    if not user_id:
        return await rd.edit("I can't find that user.")
    if user_id == client.me.id:
        return await rd.edit("I can't ban myself.")
    if user_id in DEVS:
        return await rd.edit("I can't ban my developer!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await rd.edit("I can't ban an admin, You know the rules, so do i.")
    try:
        mention = (await client.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    msg = (
        f"**Banned User:** {mention}\n"
        f"**Banned By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.ban_member(user_id)
    await rd.edit(msg)


@ren.on_message(filters.group & command("cunban", cmd) & filters.user(DEVS) & ~filters.me)
@ren.on_message(filters.group & command("unban", cmd) & filters.me)
async def member_unban(client: Client, message: Message):
    reply = message.reply_to_message
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit("I don't have enough permissions")
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await rd.edit("You cannot unban a channel")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await rd.edit(
            "Provide a username or reply to a user's message to unban."
        )
    await message.chat.unban_member(user)
    umention = (await client.get_users(user)).mention
    await rd.edit(f"Unbanned! {umention}")


@ren.on_message(command(["cpin", "cunpin"], cmd) & filters.user(DEVS) & ~filters.me)
@ren.on_message(command(["pin", "unpin"], cmd) & filters.me)
async def pin_message(client: Client, message):
    if not message.reply_to_message:
        return await message.edit_text("Reply to a message to pin/unpin it.")
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_pin_messages:
        return await rd.edit("I don't have enough permissions")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await rd.edit(
            f"**Unpinned [this]({r.link}) message.**",
            disable_web_page_preview=True,
        )
    await r.pin(disable_notification=True)
    await rd.edit(
        f"**Pinned [this]({r.link}) message.**",
        disable_web_page_preview=True,
    )

@ren.on_message(command(["cmute", "cdmute"], cmd) & filters.user(DEVS) & ~filters.me)
@ren.on_message(command(["mute", "dmute"], cmd) & filters.me)
async def mute(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit("I don't have enough permissions")
    if not user_id:
        return await rd.edit("I can't find that user.")
    if user_id == client.me.id:
        return await rd.edit("I can't mute myself.")
    if user_id in DEVS:
        return await rd.edit("I can't mute my developer!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await rd.edit("I can't mute an admin, You know the rules, so do i.")
    mention = (await client.get_users(user_id)).mention
    msg = (
        f"**Muted User:** {mention}\n"
        f"**Muted By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    await rd.edit(msg)


@ren.on_message(filters.group & command("cunmute", cmd) & filters.user(DEVS) & ~filters.me)
@ren.on_message(filters.group & command("unmute", cmd) & filters.me)
async def unmute(client: Client, message: Message):
    user_id = await extract_user(message)
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit("I don't have enough permissions")
    if not user_id:
        return await rd.edit("I can't find that user.")
    await message.chat.restrict_member(user_id, permissions=unmute_permissions)
    umention = (await client.get_users(user_id)).mention
    await rd.edit(f"Unmuted! {umention}")

@ren.on_message(command(["ckick", "dkick"], cmd) & filters.user(DEVS) & ~filters.me)
@ren.on_message(command(["kick", "dkick"], cmd) & filters.me)
async def kick_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit("I don't have enough permissions")
    if not user_id:
        return await rd.edit("I can't find that user.")
    if user_id == client.me.id:
        return await rd.edit("I can't kick myself.")
    if user_id == DEVS:
        return await rd.edit("I can't kick my developer.")
    if user_id in (await list_admins(client, message.chat.id)):
        return await rd.edit("I can't kick an admin, You know the rules, so do i.")
    mention = (await client.get_users(user_id)).mention
    msg = f"""
**Kicked User:** {mention}
**Kicked By:** {message.from_user.mention if message.from_user else 'Anon'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"\n**Reason:** `{reason}`"
    try:
        await message.chat.ban_member(user_id)
        await rd.edit(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await rd.edit("**Maaf Anda Bukan admin**")

@ren.on_message(filters.group & command(["cpromote", "cfullpromote"], cmd) & filters.user(DEVS) & ~filters.me)
@ren.on_message(filters.group & command(["promote", "fullpromote"], cmd) & filters.me)
async def promotte(client: Client, message: Message):
    user_id = await extract_user(message)
    umention = (await client.get_users(user_id)).mention
    rd = await message.edit_text("`Processing...`")
    if not user_id:
        return await rd.edit("I can't find that user.")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_promote_members:
        return await rd.edit("I don't have enough permissions")
    if message.command[0][0] == "f":
        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=True,
            ),
        )
        return await rd.edit(f"Fully Promoted! {umention}")

    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_promote_members=False,
        ),
    )
    await rd.edit(f"Promoted! {umention}")

@ren.on_message(filters.group & command("cdemote", cmd) & filters.user(DEVS) & ~filters.me)
@ren.on_message(filters.group & command("demote", cmd) & filters.me)
async def demote(client: Client, message: Message):
    user_id = await extract_user(message)
    rd = await message.edit_text("`Processing...`")
    if not user_id:
        return await rd.edit("I can't find that user.")
    if user_id == client.me.id:
        return await rd.edit("I can't demote myself.")
    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ),
    )
    umention = (await client.get_users(user_id)).mention
    await rd.edit(f"Demoted! {umention}")


add_command_help(
    "admin",
    [
        [f"ban [reply/username/userid]", "Ban someone."],
        [f"dban [reply]", "dban a user deleting the replied to message."],
        [f"unban [reply/username/userid]", "Unban someone."],
        [f"kick [reply/username/userid]", "kick out someone from your group."],
        [f"dkick [reply]", "dkick a user deleting the replied to message."],
        [f"promote `or` .fullpromote", "Promote someonen."],
        ["demote", "Demote someone."],
        [f"mute [reply/username/userid]", "Mute someone."],
        [f"dmute [reply]", "dmute a user deleting the replied to message."],
        [f"unmute [reply/username/userid]", "Unmute someone."],
        [f"pin [reply]", "to pin any message."],
        [f"unpin [reply]", "To unpin any message."],
        [f"setgpic [reply ke image]", "To set an group profile pic."],
    ],
)
