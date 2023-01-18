from pyrogram import errors, filters
from pyrogram import Client as ren
from pyrogram import Client
from pyrogram.types import ChatPermissions, Message

from pykillerx import *
from pykillerx.helper import *
from pykillerx.helper.hacking import *
from pykillerx.helper.basic import *
from pykillerx.blacklist import *
from pykillerx.help import *

from DarkWeb import *
from DarkWeb.modules.profile import extract_user, extract_user_and_reason
from DarkWeb.helper.misc import *
from DarkWeb.helper.cmd import *

# Credits: @mrismanaziz


def globals_init():
    try:
        global sql, sql2
        from importlib import import_module

        sql = import_module("DarkWeb.database.SQL.gban_sql")
        sql2 = import_module("DarkWeb.database.SQL.gmute_sql")
    except Exception as e:
        sql = None
        sql2 = None
        LOGS.warn("Unable to run GBan and GMute command, no SQL connection found")
        raise e


globals_init()


@ren.on_message(filters.command("cgban", cmd) & filters.user(DEVS) & ~filters.via_bot)
@ren.on_message(filters.command("gban", cmd) & filters.me)
async def gban_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if message.from_user.id != client.me.id:
        ren = await message.reply("`Whacking Gbanning...`")
    else:
        ren = await message.edit("`Whacking Gbanning....`")
    if not user_id:
        return await ren.edit("I can't find that user.")
    if user_id == client.me.id:
        return await ren.edit("**why bother yourself lol**")
    if user_id in DEVS:
        return await ren.edit("**failed gban because he is my creator**"
        )
    if user_id:
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await ren.edit("`Harap tentukan pengguna yang valid!`")

    if sql.is_gbanned(user.id):
        return await ren.edit(
            f"[Gbanned](tg://user?id={user.id}) **ini sudah ada di daftar gbanned**"
        )
    f_chats = await get_ub_chats(client)
    if not f_chats:
        return await ren.edit("**you do not have a group that you admin**")
    er = 0
    done = 0
    for gokid in f_chats:
        try:
            await client.ban_chat_member(chat_id=gokid, user_id=int(user.id))
            done += 1
        except BaseException:
            er += 1
    sql.gban(user.id)
    msg = (
        r"**\\#GBanned_User//**"
        f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})"
        f"\n**User ID:** `{user.id}`"
    )
    if reason:
        msg += f"\n**Reason:** `{reason}`"
    msg += f"\n**Affected To:** `{done}` **Chats**"
    await ren.edit(msg)


@ren.on_message(filters.command("cungban", ["."]) & filters.user(DEVS) & ~filters.via_bot)
@ren.on_message(filters.command("ungban", cmd) & filters.me)
async def ungban_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if message.from_user.id != client.me.id:
        ren = await message.reply("`UnGbanning...`")
    else:
        ren = await message.edit("`UnGbanning....`")
    if not user_id:
        return await ren.edit("Saya tidak dapat menemukan pengguna itu.")
    if user_id:
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await ren.edit("`Harap tentukan pengguna yang valid!`")

    try:
        if not sql.is_gbanned(user.id):
            return await ren.edit("`User already ungban`")
        ung_chats = await get_ub_chats(client)
        if not ung_chats:
            return await ren.edit("**you do not have a group that you admin**")
        er = 0
        done = 0
        for good_boi in ung_chats:
            try:
                await client.unban_chat_member(chat_id=good_boi, user_id=user.id)
                done += 1
            except BaseException:
                er += 1
        sql.ungban(user.id)
        msg = (
            r"**\\#UnGbanned_User//**"
            f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})"
            f"\n**User ID:** `{user.id}`"
        )
        if reason:
            msg += f"\n**Reason:** `{reason}`"
        msg += f"\n**Affected To:** `{done}` **Chats**"
        await ren.edit(msg)
    except Exception as e:
        await ren.edit(f"**ERROR:** `{e}`")
        return


@ren.on_message(filters.command("listgban", cmd) & filters.me)
async def gbanlist(client: Client, message: Message):
    users = sql.gbanned_users()
    ren = await edit_or_reply(message, "`Processing...`")
    if not users:
        return await ren.edit("no users have been gbanned yet")
    gban_list = "**GBanned Users:**\n"
    count = 0
    for i in users:
        count += 1
        gban_list += f"**{count} -** `{i.sender}`\n"
    return await ren.edit(gban_list)


@ren.on_message(filters.command("gmute", cmd) & filters.me)
async def gmute_user(client: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    ren = await edit_or_reply(message, "`Processing...`")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            await ren.edit(f"`Please specify a valid user!`")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await client.get_users(user_id)
    else:
        await ren.edit(f"`Please specify a valid user!`")
        return
    if user.id == client.me.id:
        return await ren.edit("**what are you doing to yourself lol**")
    if user.id in DEVS:
        return await ren.edit("**Failed to gmute because he is my maker**"
        )
    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return await ren.edit("`Calm down anybob, you can't gmute yourself.`")
    except BaseException:
        pass

    try:
        if sql2.is_gmuted(user.id):
            return await ren.edit("`User already gmuted`")
        sql2.gmute(user.id)
        await ren.edit(f"[{user.first_name}](tg://user?id={user.id}) globally gmuted!")
        try:
            common_chats = await client.get_common_chats(user.id)
            for i in common_chats:
                await i.restrict_member(user.id, ChatPermissions())
        except BaseException:
            pass
    except Exception as e:
        await ren.edit(f"**ERROR:** `{e}`")
        return


@ren.on_message(filters.command("ungmute", cmd) & filters.me)
async def ungmute_user(client: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    ren = await edit_or_reply(message, "`Processing...`")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            await ren.edit(f"`Please specify a valid user!`")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await client.get_users(user_id)
    else:
        await ren.edit(f"`Please specify a valid user!`")
        return

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return await ren.edit("`Calm down anybob, you can't ungmute yourself.`")
    except BaseException:
        pass

    try:
        if not sql2.is_gmuted(user.id):
            return await ren.edit("`User already ungmuted`")
        sql2.ungmute(user.id)
        try:
            common_chats = await client.get_common_chats(user.id)
            for i in common_chats:
                await i.unban_member(user.id)
        except BaseException:
            pass
        await ren.edit(
            f"[{user.first_name}](tg://user?id={user.id}) globally ungmuted!"
        )
    except Exception as e:
        await ren.edit(f"**ERROR:** `{e}`")
        return


@ren.on_message(filters.command("listgmute", cmd) & filters.me)
async def gmutelist(client: Client, message: Message):
    users = sql2.gmuted_users()
    ren = await edit_or_reply(message, "`Processing...`")
    if not users:
        return await ren.edit("No users have been muted yet")
    gmute_list = "**GMuted Users:**\n"
    count = 0
    for i in users:
        count += 1
        gmute_list += f"**{count} -** `{i.sender}`\n"
    return await ren.edit(gmute_list)


@ren.on_message(filters.incoming & filters.group)
async def globals_check(client: Client, message: Message):
    if not message:
        return
    if not message.from_user:
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not user_id:
        return
    if sql.is_gbanned(user_id):
        try:
            await client.ban_chat_member(chat_id, user_id)
        except BaseException:
            pass

    if sql2.is_gmuted(user_id):
        try:
            await message.delete()
        except errors.RPCError:
            pass
        try:
            await client.restrict_chat_member(chat_id, user_id, ChatPermissions())
        except BaseException:
            pass

    message.continue_propagation()


add_command_help(
    "globals",
    [
        [f"gban <reply/username/userid>", "do global banned to all groups where you as admin."],
        [f"ungban <reply/username/userid>", "cancel global banned."],
        ["listgban", "displays the global banned list."],
    ],
)
