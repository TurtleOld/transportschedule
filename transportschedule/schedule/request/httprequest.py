import httpx
from icecream import ic


async def request_schedule(link, params):
    async with httpx.AsyncClient(
        base_url='https://api.rasp.yandex.net/v3.0/',
        http2=True,
        params=params,
    ) as client:
        return await client.get(f'/{link}')
