from httpx import Response

from neuroio.api.base import APIBase, APIBaseAsync


class Whoami(APIBase):
    def me(self) -> Response:
        with self.get_client() as client:
            return client.get(url="/v1/whoami/")


class WhoamiAsync(APIBaseAsync):
    async def me(self) -> Response:
        async with self.get_client() as client:
            return await client.get(url="/v1/whoami/")
