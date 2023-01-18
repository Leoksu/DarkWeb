import asyncio
from telegraph import Telegraph, exceptions, upload_file

from pyrogram.types import *
from pyrogram import *
from pyrogram import Client as ren
from pyrogram import Client

from DarkWeb.helper.cmd import *
from DarkWeb.helper.misc import *

from pykillerx.helper.basic import *
from pykillerx.helper.hacking import *
from pykillerx import *
from pykillerx.helper import *
from pykillerx.help import *

telegraph = Telegraph()
r = telegraph.create_account(short_name="DarkWeb-Userbot")
auth_url = r["auth_url"]


@ren.on_message(filters.command(["tg", "telegraph"], cmd) & filters.me)
async def uptotelegraph(client: Client, message: Message):
    ren = await edit_or_reply(message, "`Processing . . .`")
    if not message.reply_to_message:
        await ren.edit(
            "**Please reply to the message, to get the link from the telegraph**"
        )
        return
    if message.reply_to_message.media:
        if message.reply_to_message.sticker:
            pe_ler = await convert_to_image(message, client)
        else:
            pe_ler = await message.reply_to_message.download()
        try:
            media_url = upload_file(pe_ler)
        except exceptions.TelegraphException as exc:
            await ren.edit(f"**ERROR:** `{exc}`")
            os.remove(pe_ler)
            return
        done = (
            f"**Successfully uploaded to** [Telegraph](https://telegra.ph/{media_url[0]})"
        )
        await ren.edit(done)
        os.remove(pe_ler)
    elif message.reply_to_message.text:
        page_title = get_text(message) if get_text(message) else client.me.first_name
        page_text = message.reply_to_message.text
        page_text = page_text.replace("\n", "<br>")
        try:
            response = telegraph.create_page(page_title, html_content=page_text)
        except exceptions.TelegraphException as exc:
            await ren.edit(f"**ERROR:** `{exc}`")
            return
        tele = f"**Successfully uploaded to** [Telegraph](https://telegra.ph/{response['path']})"
        await ren.edit(tele)


add_command_help(
    "telegraph",
    [
        [f"telegraph or .tg", "Reply to messages or media to upload them to the telegraph."],
    ],
)
