import asyncio
import importlib
from pyrogram import Client, idle
from pyrogram.types import *
from pyrogram import *
from DarkWeb.modules import ALL_MODULES
from DarkWeb import clients, ids, app
from pykillerx.helper import *
from config import *


async def start_bot():
    await app.start()
    print("LOG: Mendirikan Bot token Booting..")
    for all_module in ALL_MODULES:
        importlib.import_module("DarkWeb.modules" + all_module)
        print(f"Successfully Imported {all_module} 🛠️")
    for cli in clients:
        try:
            await cli.start()
            ex = await cli.get_me()
            await join(cli)
            try:
                await cli.send_photo("me", photo=LOG_ALIVE, caption=ALIVE_ONLINE)
            except BaseException:
                pass
            print(f"Started {ex.first_name} ☠️")
            ids.append(ex.id)
        except Exception as e:
            print(f"{e}")
    await idle()

loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())
