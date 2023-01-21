import random
import time
from datetime import datetime
from datetime import datetime as dt

import asyncio 
import speedtest
from pyrogram import filters
from pyrogram import Client as ren
from pyrogram import Client
from pyrogram.raw import functions
from pyrogram.types import Message

from DarkWeb import StartTime, app
from DarkWeb.modules.bot.inline import get_readable_time
from DarkWeb.helper.cmd import cmd

from pykillerx.helper.hacking import *
from pykillerx import *
from pykillerx.helper import *
from pykillerx.blacklist import *
from pykillerx.help import *
from pykillerx.helper.goblok import *

from config import *

class WWW:
    SpeedTest = (
        "Speedtest started at `{start}`\n\n"
        "Ping:\n{ping} ms\n\n"
        "Download:\n{download}\n\n"
        "Upload:\n{upload}\n\n"
        "ISP:\n__{isp}__"
    )

    NearestDC = "Country: `{}`\n" "Nearest Datacenter: `{}`\n" "This Datacenter: `{}`"

@ren.on_message(
    filters.command(["speedtest"], cmd) & filters.me)
async def speed_test(client: Client, message: Message):
    new_msg = await message.reply_text("`Running speed test . . .`")
    try:
       await message.delete()
    except:
       pass
    spd = speedtest.Speedtest()

    new_msg = await new_msg.edit(
        f"`{new_msg.text}`\n" "`Getting best server based on ping . . .`"
    )
    spd.get_best_server()

    new_msg = await new_msg.edit(f"`{new_msg.text}`\n" "`Testing download speed . . .`")
    spd.download()

    new_msg = await new_msg.edit(f"`{new_msg.text}`\n" "`Testing upload speed . . .`")
    spd.upload()

    new_msg = await new_msg.edit(
        f"`{new_msg.text}`\n" "`Getting results and preparing formatting . . .`"
    )
    results = spd.results.dict()

    await new_msg.edit(
        WWW.SpeedTest.format(
            start=results["timestamp"],
            ping=results["ping"],
            download=SpeedConvert(results["download"]),
            upload=SpeedConvert(results["upload"]),
            isp=results["client"]["isp"],
        )
    )


@ren.on_message(filters.command("cxping", cmd) & filters.user(DEVS) & ~filters.me)
@ren.on_message(filters.command(["xping"], cmd) & filters.me)
async def pingme(client: Client, message: Message):
    uptime = await get_readable_time((time.time() - StartTime))
    start = dt.now()
    xx = await message.reply_text("**0% ▒▒▒▒▒▒▒▒▒▒**")
    await xx.edit("**20% ██▒▒▒▒▒▒▒▒**")
    await xx.edit("**40% ████▒▒▒▒▒▒**")
    await xx.edit("**60% ██████▒▒▒▒**")
    await xx.edit("**80% ████████▒▒**")
    await xx.edit("**100% ██████████**")
    end = dt.now()
    duration = (end - start).microseconds / 1000
    await xx.edit(
        f"**✾𝗣𝗜𝗡𝗚𝗘𝗥✾**\n"
        f"** ▹  Sɪɢɴᴀʟ   :**"
        f"`%sms` \n"
        f"** ▹  Uᴘᴛɪᴍᴇ  :**"
        f"`{uptime}` \n"
        f"** ▹  Oᴡɴᴇʀ   :** `{client.me.mention}` \n" % (duration)
    )

""" 
credits by @xtsea
"""
@ren.on_message(filters.command("kping", cmd) & filters.me)
async def fastpin(client: Client, message: Message):
    """For .ping command, ping the userbot from any chat."""
    uptime = await get_readable_time((time.time() - StartTime))
    start = dt.now()
    await message.edit("**█▒▒▒▒▒▒▒▒▒**")
    await message.edit("**███▒▒▒▒▒▒▒**")
    await message.edit("**█████▒▒▒▒▒**")
    await message.edit("**███████▒▒▒**")
    await message.edit("**██████████**")
    await message.edit("⚡")
    await asyncio.sleep(3)
    end = dt.now()
    duration = (end - start).microseconds / 1000
    await message.edit(
        f"╔════▣**TEST** ◎ **PING**▣════╗\n"
        f"🏓 **Pɪɴɢᴇʀ :** "
        f"`%sms` \n"
        f"🎈 **Uᴘᴛɪᴍᴇ :** "
        f"`{uptime}` \n"
        f"👑 **Oᴡɴᴇʀ :** `{client.me.mention}`" % (duration)
    )

@ren.on_message(filters.regex("(?i)^ping") & filters.user(DEVS) & ~filters.me)
@ren.on_message(filters.command("ping", cmd) & filters.me)
async def zping(client: Client, message: Message):
    uptime = await get_readable_time((time.time() - StartTime))
    start = dt.now()
    lol = await message.reply_text("**Pong!!**")
    await asyncio.sleep(1.5)
    end = dt.now()
    duration = (end - start).microseconds / 1000
    await message.lol(
        f" **Pong !!** "
        f"`%sms` \n"
        f" **Uptime** - "
        f"`{uptime}` " % (duration)
    )


@ren.on_message(filters.command("palive", cmd) & filters.me)
async def palive(client: Client, message: Message):
    uptime = await get_readable_time((time.time() - StartTime))
    start = dt.now()
    lol = await message.edit("**Pong!**")
    await asyncio.sleep(1.5)
    end = dt.now()
    await lol.delete()
    duration = (end - start).microseconds / 1000
    await message.send_photo(
        message.chat.id,
        ALIVE_PIC,
        f" **Pong !!** "
        f"`%sms` \n"
        f" **Uptime** "
        f"`{uptime}` " % (duration)
    )


# credits @xtsea

@ren.on_message(filters.command(["fck"], cmd) & filters.me)
async def pingme_2(client: Client, message: Message):
    uptime = await get_readable_time((time.time() - StartTime))
    start = dt.now()
    xx = await message.reply_text("**0% ▒▒▒▒▒▒▒▒▒▒**")
    await xx.edit(".                       /¯ )")
    await xx.edit(".                       /¯ )\n                      /¯  /")
    await xx.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /"
    )
    await xx.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸"
    )
    await xx.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ "
    )
    await xx.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')"
    )
    await xx.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /"
    )
    await xx.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´"
    )
    await xx.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              ("
    )
    await xx.edit(
        ".                       /¯ )\n                      /¯  /\n                    /    /\n              /´¯/'   '/´¯¯`•¸\n          /'/   /    /       /¨¯\\ \n        ('(   (   (   (  ¯~/'  ')\n         \\                        /\n          \\                _.•´\n            \\              (\n              \\  "
    )


# by @xtsea
@ren.on_message(filters.command("cabsen", cmd) & filters.user(DEVS) & filters.me)
@ren.on_message(filters.command("absen", cmd) & filters.me)
async def absen(client: Client, message: Message):
    await message.reply_text(random.choice(absen))

# by @xtsea
@ren.on_message(filters.command("cspd", cmd) & filters.user(DEVS) & filters.me)
@ren.on_message(filters.command("spd", cmd) & filters.me)
async def absen2(client: Client, message: Message):
    await message.reply_text(random.choice(memek))

add_command_help(
    "ping",
    [
        ["ping", "Check bot alive or not."],
        ["fck", "Check fucking."],
        ["xping", "check bot xping."],
    ],
)
