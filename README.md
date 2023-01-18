### DarkWeb

![Python Version](https://img.shields.io/badge/python-3.9-green?style=for-the-badge&logo=appveyor)
![Issues](https://img.shields.io/github/issues/TeamKillerX/DarkWeb?style=for-the-badge&logo=appveyor)
![Forks](https://img.shields.io/github/forks/TeamKillerX/DarkWeb?style=for-the-badge&logo=appveyor)
![Stars](https://img.shields.io/github/stars/TeamKillerX/DarkWeb?style=for-the-badge&logo=appveyor)
![Contributors](https://img.shields.io/github/contributors/TeamKillerX/DarkWeb?style=for-the-badge&logo=appveyor)
![Repository Size](https://img.shields.io/github/repo-size/TeamKillerX/DarkWeb?style=for-the-badge&logo=appveyor)
[![Docker Pulls](https://img.shields.io/docker/pulls/rendyprojects/python)](https://hub.docker.com/r/rendyprojects/python/tags)

## Disclaimer
```
️                       ⚠️ WARNING FOR YOU ️ ️⚠️
   DarkWeb is used to help your account activities on Telegram
   We are not responsible for what you misuse in this repository
   !  Be careful when using this repository!
   If one of the members misuses this repository, we are forced to ban you
   Never ever abuse this repository
``` 

## How to make a module
- try example use `test.py`
```python
import asyncio
from pyrogram import Client as ren
from pyrogram.types import *
from pyrogram import Client
from DarkWeb.helper.misc import *
from DarkWeb.helper.cmd import *
from pykillerx.help import *
from pykillerx.helper.basic import *
from pykillerx.helper import *


@ren.on_message(filters.command("test", cmd) & filters.me)
async def test(client: Client, message: Message):
    await client.send_message(message.chat.id, "Hello World")

add_command_help(
    "test",
    [
        ["test", "Hello World"],
    ],
)
```


### Tutorial VPS
```console
Rendy@Ubuntu~ $ sudo apt update && sudo apt upgrade -y && sudo apt-get install -y curl git npm screen ffmpeg && sudo apt-get install python3-pip -y
Rendy@Ubuntu~ $ git clone https://github.com/TeamKillerX/DarkWeb && cd DarkWeb
Rendy@Ubuntu~ $ pip3 install -r req *
Rendy@Ubuntu~ $ cp sample_config.env config.env
Rendy@Ubuntu~ $ nano config.env
Rendy@Ubuntu~ $ screen -S dark 
Rendy@Ubuntu~ $ python3 -m DarkWeb

# ctrl a + d 
```

### Heroku Manual Linux
```console
Rendy@Ubuntu~ $ git clone example-app
Rendy@Ubuntu~ $ cd example-app
Rendy@Ubuntu~ $ heroku login
Rendy@Ubuntu~ $ heroku create --region eu appname # create app in eu region, common regions: eu, us
Rendy@Ubuntu~ $ heroku buildpacks:set heroku/python # set python buildpack
Rendy@Ubuntu~ $ git push heroku master # deploy app to heroku
Rendy@Ubuntu~ $ heroku config:set EXAMPLE_BOT=123456789 # set config vars, insert your own
                ...
Rendy@Ubuntu~ $ heroku ps:scale example=1 # start bot dyno
Rendy@Ubuntu~ $ heroku logs --tail # If for some reason it’s not working, check the logs
Rendy@Ubuntu~ $ heroku ps:stop example # stop bot dyno
```

## Installling
```
pip3 install pykillerx
```

### Credits
- [DarkWeb](https://github.com/TeamKillerX/DarkWeb)
- [Zaid-Userbot](https://github.com/ITZ-ZAID/ZAID-USERBOT)
- [PyroMan-Userbot](https://github.com/mrismanaziz/PyroMan-Userbot)

## Library 
- [Pyrogram](https://github.com/pyrogram)

### Donation
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.buymeacoffee.com/randydev)
