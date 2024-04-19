import aiohttp


class Client:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    # def __del__(self):
    #     # так делать нельзя
    #     await self.session.close()

    # async def __del__(self):
    #     # так тоже нельзя
    #     await self.session.close()
