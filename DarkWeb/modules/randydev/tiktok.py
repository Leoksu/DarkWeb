"""
COPYRIGHT 2020 - 2023 : https://github.com/TeamKillerX/DarkWeb
CREDITS DEVELOPER BY : @XTSEA
"""

import subprocess, yt_dlp 
import requests 
import json
from pyrogram import *
from pyrogram.types import *
from pyrogram import Client as ren 

from DarkWeb.helper.cmd import *
from DarkWeb.helper.misc import *

from pykillerx import *
from pykillerx.helper import *
from pykillerx.helper.basic import *
from pykillerx.helper.hacking import *
from pykillerx.help import *

@ren.on_message(filters.command("ptok", cmd) & filters.me)
async def tiktok(client: Client, message: Message):
    lol = await message.reply_text("**Prossing......**")
    link = get_arg(message)
    url = requests.get(f"https://api.douyin.wtf/api?url={link}").json()
    if link:
        try:
           prik = url["nwm_video_url"]
           await client.send_video(message.chat.id, prik)
        except Exception as e:
            return await lol.edit(f"**ERROR** `{e}`")

@ren.on_message(filters.command("tvideo", cmd) & filters.me)
async def tvideo(client: Client, message: Message):
    ah = await message.reply_text("**Prossing....**")
    link = get_arg(message)
    caption = f"""
Upload By {client.me.mention}

Tiktok By [API DOUYIN](douyin.wtf)
"""
    try:
       no_youtube = "https://www.youtube.com/watch?v="
       if link not in no_youtube:
           await ah.delete()
           await client.send_video(message.chat.id, link, caption)
       else:
           await client.send_video(message.chat.id, link, caption)
    except Exception as e:
        return await send_message(messsge.chat.id, f"**ERROR** `{e}`")
