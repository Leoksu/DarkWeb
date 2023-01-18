"""
CREATE BY @XTSEA
"""

from pyrogram import Client
from pyrogram import Client as ren
from pyrogram import *
from pyrogram.types import *
from sqlalchemy.exc import IntegrityError

from DarkWeb.helper.cmd import *
from DarkWeb import *
from DarkWeb.helper.misc import *

from pykillerx import *
from pykillerx.helper import *
from pykillerx.helper.basic import *
from pykillerx.blacklist import *
from pykillerx.help import *


from DarkWeb.database.SQL.globals import addgvar, gvarstatus

DEF_UNAPPROVED_MSG = (
    "╔════════════════════╗\n"
    "     ❕ 𝗔𝗧𝗧𝗘𝗡𝗧𝗜𝗢𝗡 𝗣𝗟𝗘𝗔𝗦𝗘 ❕\n"
    "╚════════════════════╝\n"
    "• I haven't approved you to pm.\n"
    "• Wait until I approve your PM.\n"
    "• Don't Spam the chat or you will be automatically banned.\n"
    "╔════════════════════╗\n"
    "    𝗔𝘂𝘁𝗼𝗺𝗮𝘁𝗶𝗰 𝗠𝗲𝘀𝘀𝗮𝗴𝗲𝘀 𝗕𝘆 -𝗨𝘀𝗲𝗿𝗕𝗼𝘁\n"
    "╚════════════════════╝\n"
)


@ren.on_message(
    ~filters.me & filters.private & ~filters.bot & filters.incoming, group=69
)
async def incomingpm(client: Client, message: Message):
    try:
        from DarkWeb.database.SQL.globals import gvarstatus
        from DarkWeb.database.SQL.pm_permit_sql import is_approved
    except BaseException:
        pass

    if gvarstatus("PMPERMIT") and gvarstatus("PMPERMIT") == "false":
        return
    if await auto_accept(client, message) or message.from_user.is_self:
        message.continue_propagation()
    if message.chat.id != 777000:
        PM_LIMIT = gvarstatus("PM_LIMIT") or 5
        getmsg = gvarstatus("unapproved_msg")
        if getmsg is not None:
            UNAPPROVED_MSG = getmsg
        else:
            UNAPPROVED_MSG = DEF_UNAPPROVED_MSG

        apprv = is_approved(message.chat.id)
        if not apprv and message.text != UNAPPROVED_MSG:
            if message.chat.id in TEMP_SETTINGS["PM_LAST_MSG"]:
                prevmsg = TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id]
                if message.text != prevmsg:
                    async for message in client.search_messages(
                        message.chat.id,
                        from_user="me",
                        limit=10,
                        query=UNAPPROVED_MSG,
                    ):
                        await message.delete()
                    if TEMP_SETTINGS["PM_COUNT"][message.chat.id] < (int(PM_LIMIT) - 1):
                        ret = await message.reply_text(UNAPPROVED_MSG)
                        TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id] = ret.text
            else:
                ret = await message.reply_text(UNAPPROVED_MSG)
                if ret.text:
                    TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id] = ret.text
            if message.chat.id not in TEMP_SETTINGS["PM_COUNT"]:
                TEMP_SETTINGS["PM_COUNT"][message.chat.id] = 1
            else:
                TEMP_SETTINGS["PM_COUNT"][message.chat.id] = (
                    TEMP_SETTINGS["PM_COUNT"][message.chat.id] + 1
                )
            if TEMP_SETTINGS["PM_COUNT"][message.chat.id] > (int(PM_LIMIT) - 1):
                await message.reply("**Sorry you have been blocked due to spam chat**")
                try:
                    del TEMP_SETTINGS["PM_COUNT"][message.chat.id]
                    del TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id]
                except BaseException:
                    pass

                await client.block_user(message.chat.id)

    message.continue_propagation()


async def auto_accept(client, message):
    try:
        from DarkWeb.database.SQL.pm_permit_sql import approve, is_approved
    except BaseException:
        pass

    if message.chat.id in DEVS:
        try:
            approve(message.chat.id)
            await client.send_message(
                message.chat.id,
                f"<b>Receiving Messages!!!</b>\n{message.from_user.mention} <b>Developer detected DarkWeb-Userbot</b>",
                parse_mode=enums.ParseMode.HTML,
            )
        except IntegrityError:
            pass
    if message.chat.id not in [client.me.id, 777000]:
        if is_approved(message.chat.id):
            return True

        async for msg in client.get_chat_history(message.chat.id, limit=1):
            if msg.from_user.id == client.me.id:
                try:
                    del TEMP_SETTINGS["PM_COUNT"][message.chat.id]
                    del TEMP_SETTINGS["PM_LAST_MSG"][message.chat.id]
                except BaseException:
                    pass

                try:
                    approve(chat.id)
                    async for message in client.search_messages(
                        message.chat.id,
                        from_user="me",
                        limit=10,
                        query=UNAPPROVED_MSG,
                    ):
                        await message.delete()
                    return True
                except BaseException:
                    pass

    return False


@ren.on_message(
    filters.command(["ok", "setuju", "approve"], cmd) & filters.me & filters.private
)
async def approvepm(client: Client, message: Message):
    try:
        from DarkWeb.database.SQL.pm_permit_sql import approve
    except BaseException:
        await message.edit("Running on Non-SQL mode!")
        return

    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            await message.edit("You can't approve yourself.")
            return
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        uid = replied_user.id
    else:
        aname = message.chat
        if not aname.type == enums.ChatType.PRIVATE:
            await message.edit(
                "You are currently not in pm and you have not replied to someone's message."
            )
            return
        name0 = aname.first_name
        uid = aname.id

    try:
        approve(uid)
        await message.edit(f"**Receive messages from** [{name0}](tg://user?id={uid})!")
    except IntegrityError:
        await message.edit(
            f"[{name0}](tg://user?id={uid}) probably already approved for pm."
        )
        return


@ren.on_message(
    filters.command(["tolak", "nopm", "disapprove"], cmd) & filters.me & filters.private
)
async def disapprovepm(client: Client, message: Message):
    try:
        from DarkWeb.database.SQL.pm_permit_sql import dissprove
    except BaseException:
        await message.edit("Running on Non-SQL mode!")
        return

    if message.reply_to_message:
        reply = message.reply_to_message
        replied_user = reply.from_user
        if replied_user.is_self:
            await message.edit("you can't deny yourself.")
            return
        aname = replied_user.id
        name0 = str(replied_user.first_name)
        uid = replied_user.id
    else:
        aname = message.chat
        if not aname.type == enums.ChatType.PRIVATE:
            await message.edit(
                "You are not currently in PM and you have not replied to someone's message."
            )
            return
        name0 = aname.first_name
        uid = aname.id

    dissprove(uid)

    await message.edit(
        f"**Pesan** [{name0}](tg://user?id={uid}) **Completely rejected, Please don't Spam Chat!**"
    )


@ren.on_message(filters.command("pmlimit", cmd) & filters.me)
async def setpm_limit(client: Client, cust_msg: Message):
    if gvarstatus("PMPERMIT") and gvarstatus("PMPERMIT") == "false":
        return await cust_msg.edit(
            f"**You Must Set Var** `PM_AUTO_BAN` **Ke** `True`\n\n**If you want to Activate PMPERMIT, please type:** `.setvar PM_AUTO_BAN True`"
        )
    try:
        from DarkWeb.database.SQL.globals import addgvar
    except AttributeError:
        await cust_msg.edit("**Running on Non-SQL mode!**")
        return
    input_str = (
        cust_msg.text.split(None, 1)[1]
        if len(
            cust_msg.command,
        )
        != 1
        else None
    )
    if not input_str:
        return await cust_msg.edit("**Please enter a number for PM_LIMIT.**")
    ren = await cust_msg.edit("`Processing...`")
    if input_str and not input_str.isnumeric():
        return await ren.edit("**Please enter a number for PM_LIMIT**")
    addgvar("PM_LIMIT", input_str)
    await ren.edit(f"**Set PM limit to** `{input_str}`")


@ren.on_message(filters.command(["pmpermit", "pmguard"], cmd) & filters.me)
async def onoff_pmpermit(client: Client, message: Message):
    input_str = get_arg(message)
    if input_str == "off":
        h_type = False
    elif input_str == "on":
        h_type = True
    if gvarstatus("PMPERMIT") and gvarstatus("PMPERMIT") == "false":
        PMPERMIT = False
    else:
        PMPERMIT = True
    if PMPERMIT:
        if h_type:
            await edit_or_reply(message, "**PMPERMIT Already Activated**")
        else:
            addgvar("PMPERMIT", h_type)
            await edit_or_reply(message, "**PMPERMIT Successfully turned off**")
    elif h_type:
        addgvar("PMPERMIT", h_type)
        await edit_or_reply(message, "**PMPERMIT Successfully activated**")
    else:
        await edit_or_reply(message, "**PMPERMIT It's turned off**")


@ren.on_message(filters.command("setpmpermit", cmd) & filters.me)
async def setpmpermit(client: Client, cust_msg: Message):
    """Set your own Unapproved message"""
    if gvarstatus("PMPERMIT") and gvarstatus("PMPERMIT") == "false":
        return await cust_msg.edit(
            "**You Must Set Var** `PM_AUTO_BAN` **Ke** `True`\n\n**If you want to activate PMPERMIT, please type:** `.setvar PM_AUTO_BAN True`"
        )
    try:
        import DarkWeb.database.SQL.globals as sql
    except AttributeError:
        await cust_msg.edit("**Running on Non-SQL mode!**")
        return
    ren = await cust_msg.edit("`Processing...`")
    custom_message = sql.gvarstatus("unapproved_msg")
    message = cust_msg.reply_to_message
    if custom_message is not None:
        sql.delgvar("unapproved_msg")
    if not message:
        return await ren.edit("**Please Reply to the message**")
    msg = message.text
    sql.addgvar("unapproved_msg", msg)
    await ren.edit("**Message Successfully saved to chat room**")


@ren.on_message(filters.command("getpmpermit", cmd) & filters.me)
async def get_pmermit(client: Client, cust_msg: Message):
    if gvarstatus("PMPERMIT") and gvarstatus("PMPERMIT") == "false":
        return await cust_msg.edit(
            "**You have to set var** `PM_AUTO_BAN` **Ke** `True`\n\n**If you want to Activate PMPERMIT, please type:** `.setvar PM_AUTO_BAN True`"
        )
    try:
        import DarkWeb.database.SQL.globals as sql
    except AttributeError:
        await cust_msg.edit("**Running on Non-SQL mode!**")
        return
    ren = await cust_msg.edit("`Processing...`")
    custom_message = sql.gvarstatus("unapproved_msg")
    if custom_message is not None:
        await ren.edit("**Order PMPERMIT now:**" f"\n\n{custom_message}")
    else:
        await ren.edit(
            "**You have not set PMPERMIT custom messages,**\n"
            f"**Still using Default PM Messages:**\n\n{DEF_UNAPPROVED_MSG}"
        )


@ren.on_message(filters.command("resetpmpermit", cmd) & filters.me)
async def reset_pmpermit(client: Client, cust_msg: Message):
    if gvarstatus("PMPERMIT") and gvarstatus("PMPERMIT") == "false":
        return await cust_msg.edit(
            f"**You Must Set var** `PM_AUTO_BAN` **Ke** `True`\n\n**If you want to Activate PMPERMIT, please type:** `.setvar PM_AUTO_BAN True`"
        )
    try:
        import DarkWeb.database.SQL.globals as sql
    except AttributeError:
        await cust_msg.edit("**Running on Non-SQL mode!**")
        return
    ren = await cust_msg.edit("`Processing...`")
    custom_message = sql.gvarstatus("unapproved_msg")

    if custom_message is None:
        await ren.edit("**Your PMPERMIT message is default**")
    else:
        sql.delgvar("unapproved_msg")
        await ren.edit("**Successfully Changed PMPERMIT custom message to default**")


add_command_help(
    "pmpermit",
    [
        [f"ok atau .setuju", "Receive someone's message by replying to the message or tagging and also to do it in PMM"],
        [f"tolak atau .nopm", "Reject someone's message by replying to the message or tagging and also to do it in PM"],
        [f"pmlimit <number>", "To customize messages, limit auto block messages"],
        [f"setpmpermit <reply to message>", "To customize PMPERMIT messages for people whose messages have not been received"],
        ["getpmpermit", "To view PMPERMIT messages"],
        ["resetpmpermit", "To reset PMPERMIT messages to DEFAULT"],
        [f"pmpermit on/off", "To enable or disable PMPERMIT"],
    ],
)
