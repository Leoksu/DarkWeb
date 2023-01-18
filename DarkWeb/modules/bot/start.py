# Credits: @xtsea
# please do not remove credits 
# copyright https://github.com/TeamKillerX

from pyrogram import *
from pyrogram import Client
from pyrogram.types import *

@Client.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):
    welcome = f"""
Hey there! {message.from_user.mention}
I'm an <b>administration</b> bot that helps you to keep your groups safe from <b>spammers</b>
If you want to use me for your groups, note that I'm more useful on a pyrogram of groups and you also need to <b>setup a new bot.</b>
So if you don't wish to self-host, @MissRose_bot might be a better choice for
"""
    try:
        await message.reply_text(
            text=welcome,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🛠️ Source",
                            url="https://github.com/TeamKillerX/",
                        )
                   ],
                ]
            ),
        )
    except Exception:
        pass
