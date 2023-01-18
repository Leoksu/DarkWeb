# hacker by @xtsea
# copyright 2020 - 2023 : https://github.com/TeamKillerX/

import requests
import os
import json
import random
from pyrogram import *
from pyrogram.types import *
from pyrogram import Client as ren 
from pyrogram.errors import MessageNotModified
from DarkWeb.helper.what import *
from DarkWeb.helper.cmd import *

from pykillerx.helper import *
from pykillerx.help import *
from pykillerx.helper.tools import *
from pykillerx import *

from config import OPENAI_API

@ren.on_message(filters.command("cask", cmd) & filters.user(901878554) & ~filters.me)
@ren.on_message(filters.command("ask", cmd) & filters.me)
async def openai(c, m):
    if len(m.command) == 1:
        return await m.reply(f"use command <code>.{m.command[0]} [question]</code> to ask questions using the API.")
    question = m.text.split(" ", maxsplit=1)[1]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API}",
    }

    json_data = {
        "model": "text-davinci-003",
        "prompt": question,
        "max_tokens": 200,
        "temperature": 0,
    }
    msg = await m.reply("Wait a moment looking for your answer..")
    try:
        response = (await http.post("https://api.openai.com/v1/completions", headers=headers, json=json_data)).json()
        await msg.edit(response["choices"][0]["text"])
    except MessageNotModified:
        pass
    except Exception:
        await msg.edit("Yahh, sorry i can't get your answer.")

add_command_help(
    "chatbot",
    [
        [f"ask [question]", "to ask questions using the API."],
    ],
)
