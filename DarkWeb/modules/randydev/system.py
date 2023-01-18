import sys
from os import environ, execle, remove
from pyrogram import *
from pyrogram.types import *
from pyrogram import Client as ren
from pyrogram import Client
from DarkWeb.helper.cmd import *
from DarkWeb import *
from DarkWeb.helper.misc import *

from pykillerx.helper.basic import *
from pykillerx import *
from pykillerx.helper import *
from pykillerx.help import *

@Client.on_message(filters.command("restart", cmd) & filters.user(1191668125))
async def restart_bot(_, message: Message):
    try:
        msg = await edit_or_reply(message, "`Restarting bot...`")
        LOGGER("DarkWeb").info("BOT SERVER RESTARTED !!")
    except BaseException as err:
        LOGGER("DarkWeb").info(f"{err}")
        return
    await msg.edit_text("✅ Bot has restarted !\n\n")
    if HAPP is not None:
        HAPP.restart()
    else:
        args = [sys.executable, "-m", "DarkWeb"]
        execle(sys.executable, *args, environ)



add_command_help(
    "system",
    [
        ["restart", "to restart userbot."],
    ],
)
