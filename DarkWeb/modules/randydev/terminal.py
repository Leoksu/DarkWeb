from pyrogram import *
from pyrogram.types import *
from pyrogram import Client as ren 
from KillerXBase.helper.cmd import *
from KillerXBase.helper.misc import *

from pykillerx import *
from pykillerx.helper.basic import *
from pykillerx.helper.hacking import *
from pykillerx.helper import *
from pykillerx.help import *

# like this utroid using terminal file upload
# credits @xtsea // please do not remove credits

@ren.on_message(filters.command("ul", cmd) & filters.me)
async def terminal(client: Client, message: Message):
    file = get_arg(message)
    vcs = await message.reply_text("**please wait a moment for the file to upload....**")
    await asyncio.sleep(2)
    await vcs.edit("**Uploaded successfully...**")
    if file:
        try:
           await client.send_document(message.chat.id, file)
        except Exception as e:
            return await vcs.edit(f"**ERROR** `{e}`") 

add_command_help(
    "terminal",
    [
        [f"ul [exec]", "using terminal/shell example: `.ul file/to/path/name.py`"],
    ],
)
