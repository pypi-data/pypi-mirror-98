from httpx import Response

from neuroio.api.base import APIBase, APIBaseAsync


class Spaces(APIBase):
    def create(self, name: str) -> Response:
        data = {"name": name}

        with self.get_client() as client:
            return client.post(url="/v1/spaces/", json=data)

    def list(
        self, q: str = None, limit: int = 20, offset: int = 0
    ) -> Response:
        data = {"q": q, "limit": limit, "offset": offset}

        with self.get_client() as client:
            return client.get(url="/v1/spaces/", params=data)

    def get(self, id: int) -> Response:
        with self.get_client() as client:
            return client.get(url=f"/v1/spaces/{id}/")

    def update(self, id: int, name: str) -> Response:
        data = {"name": name}

        with self.get_client() as client:
            return client.patch(url=f"/v1/spaces/{id}/", json=data)

    def delete(self, id: int) -> Response:
        with self.get_client() as client:
            return client.delete(url=f"/v1/spaces/{id}/")

    def token(self, id: int, permanent: bool = False) -> Response:
        data = {"permanent": permanent}

        with self.get_client() as client:
            return client.post(url=f"/v1/spaces/{id}/tokens/", json=data)


class SpacesAsync(APIBaseAsync):
    async def create(self, name: str) -> Response:
        data = {"name": name}

        async with self.get_client() as client:
            return await client.post(url="/v1/spaces/", json=data)

    async def list(
        self, q: str = None, limit: int = 20, offset: int = 0
    ) -> Response:
        data = {"q": q, "limit": limit, "offset": offset}

        async with self.get_client() as client:
            return await client.get(url="/v1/spaces/", params=data)

    async def get(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.get(url=f"/v1/spaces/{id}/")

    async def update(self, id: int, name: str) -> Response:
        data = {"name": name}

        async with self.get_client() as client:
            return await client.patch(url=f"/v1/spaces/{id}/", json=data)

    async def delete(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.delete(url=f"/v1/spaces/{id}/")

    async def token(self, id: int, permanent: bool = False) -> Response:
        data = {"permanent": permanent}
        async with self.get_client() as client:
            return await client.post(url=f"/v1/spaces/{id}/tokens/", json=data)
