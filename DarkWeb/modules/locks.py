from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    ChatNotModified,
)
from pyrogram.types import ChatPermissions, Message
from pyrogram import Client as ren

from DarkWeb.helper.cmd import *
from DarkWeb import *

from pykillerx import *
from pykillerx.helper.tools import *
from pykillerx.helper import *
from pykillerx.help import *


@ren.on_message(filters.command(["lock", "unlock"], cmd) & filters.me)
async def locks_func(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.edit_text(incorrect_parameters)
    chat_id = message.chat.id
    parameter = message.text.strip().split(None, 1)[1].lower()
    state = message.command[0].lower()
    if parameter not in data and parameter != "all":
        return await message.edit_text(incorrect_parameters)
    permissions = await current_chat_permissions(client, chat_id)
    if parameter in data:
        await tg_lock(
            client,
            message,
            parameter,
            permissions,
            data[parameter],
            bool(state == "lock"),
        )
    elif parameter == "all" and state == "lock":
        try:
            await client.set_chat_permissions(chat_id, ChatPermissions())
            await message.edit_text(
                f"🔒 **Locked for non-admin!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
            )
        except ChatAdminRequired:
            return await message.edit_text("`I don't have permission to do that.`")
        except ChatNotModified:
            return await message.edit_text(
                f"🔒 **Already locked!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
            )
    elif parameter == "all" and state == "unlock":
        try:
            await client.set_chat_permissions(
                chat_id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_send_polls=True,
                    can_change_info=False,
                    can_invite_users=True,
                    can_pin_messages=False,
                ),
            )
        except ChatAdminRequired:
            return await message.edit_text("`I don't have permission to do that.`")
        await message.edit(
            f"🔒 **Unlocked for non-admin!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
        )


@ren.on_message(filters.command("locks", cmd) & filters.me)
async def locktypes(client: Client, message: Message):
    permissions = await current_chat_permissions(client, message.chat.id)

    if not permissions:
        return await message.edit("🔒 **Everything is locked!**")

    perms = ""
    for i in permissions:
        perms += f" • __**{i}**__\n"

    await message.edit_text(perms)


add_command_help(
    "locks",
    [
        ["lock [all or specific]", "restrict user to send."],
        [
            "unlock [all or specific]",
            "Unrestrict\n\nSupported Locks / Unlocks:` `msg` | `media` | `stickers` | `polls` | `info`  | `invite` | `webprev` |`pin` | `all`.",
        ],
    ],
)
