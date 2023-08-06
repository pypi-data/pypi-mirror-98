import asyncio
import datetime as dt
from typing import TypeVar, Any

from highwire.events import Event
from highwire.streams import AsyncStream

X = TypeVar("X")
Y = TypeVar("Y")


async def tick(start: int, delay: dt.timedelta) -> AsyncStream[int]:
    current = start
    while True:
        yield Event(value=None, occurred_at=current, received_at=current)
        await asyncio.sleep(delay.total_seconds())
        current += round(delay.total_seconds() * 1000)


async def merge(x: AsyncStream[X], y: asyncio.Queue) -> AsyncStream[Any]:
    queue: asyncio.Queue = asyncio.Queue()

    async def insert_it(z):
        async for e in z:
            await queue.put(e)

    async def insert_queue(z):
        while True:
            e = await z.get()
            await queue.put(e)

    asyncio.create_task(insert_it(x))
    asyncio.create_task(insert_queue(y))

    while True:
        yield await queue.get()
