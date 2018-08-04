from aiohttp import ClientSession, ClientResponse


class RemoteLogger(object):
    def __init__(self, base_url: str, token: str):
        self.base_url: str = base_url
        self.token: str = token
        self.session: ClientSession = None

    async def login(self):
        self.session: ClientSession = ClientSession(headers=dict(Authorization=self.token))

    async def verify(self):
        return await self.get('api/verify')

    async def log(self, template, **kwargs):
        return await self.post(f'api/logs/{template}', data=kwargs)

    async def get(self, url):
        async with self.session.get(self.base_url + '/' + url + '/') as resp:
            resp: ClientResponse = resp
            resp.raise_for_status()
            return await resp.json()

    async def post(self, url, data):
        async with self.session.post(self.base_url + '/' + url + '/', data=data) as resp:
            resp: ClientResponse = resp
            resp.raise_for_status()
            return await resp.json()
