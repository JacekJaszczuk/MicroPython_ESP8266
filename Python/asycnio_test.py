# Test biblioteki asyncio.
import uasyncio as asyncio
#import asyncio

async def bar():
    count = 0
    while True:
        count += 1
        print(count)
        await asyncio.sleep(1)  # Pause 1s

async def barr():
    count = 0
    while True:
        count += 1
        print(count)
        await asyncio.sleep(3)  # Pause 1s

loop = asyncio.get_event_loop()
loop.create_task(bar()) # Schedule ASAP
loop.create_task(barr())
loop.run_forever()