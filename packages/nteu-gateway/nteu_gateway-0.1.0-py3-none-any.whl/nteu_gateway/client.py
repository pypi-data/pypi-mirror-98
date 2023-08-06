from typing import List, Optional
import aiohttp
import asyncio


class NTEUGatewayClient:
    def __init__(self,
                 base_url: str,
                 api_version):
        self._base_url = base_url
        self._api_version = api_version

    def get_base_url(self) -> str:
        return self._base_url
    base_url = property(get_base_url)

    async def translate(self, texts: List[str], priority: Optional[int] = None, timeout: int = 300):
        data = {
            "texts": texts
        }
        if priority is not None:
            data['priority'] = priority

        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
                async with session.post(
                        f'{self._base_url}/api/{self._api_version}/translate',
                        json=data) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        print(response.status)
                        response = await response.text()
                        print(response)
        except asyncio.TimeoutError:
            pass

