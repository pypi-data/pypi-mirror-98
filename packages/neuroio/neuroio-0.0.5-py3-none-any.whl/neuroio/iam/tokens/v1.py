from typing import Union

from httpx import Response

from neuroio.api.base import APIBase, APIBaseAsync


class Tokens(APIBase):
    def create(self, permanent: bool = False) -> Response:
        data = {"permanent": permanent}

        with self.get_client() as client:
            return client.post(url="/v1/tokens/", json=data)

    def list(
        self, permanent: bool = None, limit: int = 20, offset: int = 0
    ) -> Response:
        data = {"permanent": permanent, "limit": limit, "offset": offset}

        with self.get_client() as client:
            return client.get(url="/v1/tokens/", params=data)

    def get(self, token_id_or_key: Union[int, str]) -> Response:
        with self.get_client() as client:
            return client.get(url=f"/v1/tokens/{token_id_or_key}/")

    def update(
        self, token_id_or_key: Union[int, str], is_active: bool
    ) -> Response:
        with self.get_client() as client:
            return client.patch(
                url=f"/v1/tokens/{token_id_or_key}/",
                data={"is_active": is_active},
            )

    def delete_list(self, permanent: bool = None) -> Response:
        data = {"permanent": permanent} if permanent is not None else None

        with self.get_client() as client:
            return client.delete(url="/v1/tokens/", params=data)

    def delete(self, token_id_or_key: Union[int, str]) -> Response:
        with self.get_client() as client:
            return client.delete(url=f"/v1/tokens/{token_id_or_key}/")


class TokensAsync(APIBaseAsync):
    async def create(self, permanent: bool = False) -> Response:
        data = {"permanent": permanent}

        async with self.get_client() as client:
            return await client.post(url="/v1/tokens/", json=data)

    async def list(
        self, permanent: bool = None, limit: int = 20, offset: int = 0
    ) -> Response:
        data = {"permanent": permanent, "limit": limit, "offset": offset}

        async with self.get_client() as client:
            return await client.get(url="/v1/tokens/", params=data)

    async def get(self, token_id_or_key: Union[int, str]) -> Response:
        async with self.get_client() as client:
            return await client.get(url=f"/v1/tokens/{token_id_or_key}/")

    async def update(
        self, token_id_or_key: Union[int, str], is_active: bool
    ) -> Response:
        async with self.get_client() as client:
            return await client.patch(
                url=f"/v1/tokens/{token_id_or_key}/",
                data={"is_active": is_active},
            )

    async def delete_list(self, permanent: bool = None) -> Response:
        data = {"permanent": permanent} if permanent is not None else None

        async with self.get_client() as client:
            return await client.delete(url="/v1/tokens/", params=data)

    async def delete(self, token_id_or_key: Union[int, str]) -> Response:
        async with self.get_client() as client:
            return await client.delete(url=f"/v1/tokens/{token_id_or_key}/")
