import aiohttp
import asyncio


class Client:
    def __init__(self):
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self.session

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()


async def main():
    async with Client() as session:
        async with session.get('https://api.binance.com/api/v3/depth?symbol=BTCUSDT') as response:
            data = await response.json()
            print(data)


if __name__ == "__main__":
    asyncio.run(main())
