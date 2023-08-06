import asyncio

from .search import search


async def main():
    src = await search("обезьяны")
    print(src)


asyncio.run(main())
