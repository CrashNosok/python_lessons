import asyncio

from aiohttp import ClientSession
from aiohttp_proxy import ProxyConnector

from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.net.signer.stark_curve_signer import StarkCurveSigner


class StarknetClient:
    chain_id = StarknetChainId.MAINNET
    NODE_URL = 'https://starknet-mainnet.public.blastapi.io'

    def __init__(self, private_key: int, account_address: int, proxy: str = ''):
        self.key_pair = KeyPair.from_private_key(private_key)
        self.signer = StarkCurveSigner(account_address, self.key_pair, StarknetClient.chain_id)

        self.proxy = proxy

        self.connector = None
        self.session = None
        self.starknet_client = None
        self.account = None

        if not self.proxy:
            self.starknet_client = FullNodeClient(node_url=StarknetClient.NODE_URL)
        else:
            self.connector = ProxyConnector.from_url(self.proxy)
            self.session = ClientSession(connector=self.connector)
            self.starknet_client = FullNodeClient(
                node_url=StarknetClient.NODE_URL,
                session=self.session
            )

        self.account = Account(
            address=account_address,
            client=self.starknet_client,
            key_pair=self.key_pair,
            chain=StarknetClient.chain_id
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.proxy:
            await self.session.close()


async def main():
    async with StarknetClient(
            private_key=123456789,
            account_address=123456789,
            proxy='http://login:password@ip:port'
    ) as client:
        ...


if __name__ == '__main__':
    asyncio.run(main())
