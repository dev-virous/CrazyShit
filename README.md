# CrazyShit

CrazyShit is a Python library for handling automation tasks for a WhatsApp bot using Selenium.

## Example Usage

```python
from crazyshit import Client, filters
import asyncio

client = Client(
    "test",
    number="+2011111",
)

@client.on_message(filters.regex(r"^/start$"))
async def start_(bot, msg):
    await bot.send_message(
        to=msg.chat.title,
        text="how are you?"
    )

async def run():
    await client.start()
    print("[!] Running")

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
loop.run_forever()
```

## Features
- automation tasks for a WhatsApp bot using Selenium.
- Get updates and send messages.

## Requirements
- Python 3.8 or higher.
- Selenium

## Installing
``` bash
pip3 install crazyshit
```
