import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.binance.com/api/v3/depth?symbol=BTCUSDT') as response:
            data = await response.json()
            print(data)


if __name__ == "__main__":
    asyncio.run(main())
