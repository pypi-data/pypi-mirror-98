from typing import List, Union

from httpx import Response

from neuroio.api.base import APIBase, APIBaseAsync
from neuroio.constants import sentinel
from neuroio.utils import request_query_processing


class Groups(APIBase):
    def create(self, name: str) -> Response:
        data = {"name": name}
        with self.get_client() as client:
            return client.post(url="/v1/groups/persons/", json=data)

    def list(
        self,
        q: Union[str, object] = sentinel,
        pids_include: Union[List[str], object] = sentinel,
        pids_exclude: Union[List[str], object] = sentinel,
        groups_ids: Union[List[int], object] = sentinel,
        spaces_ids: Union[List[int], object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self"])
        with self.get_client() as client:
            return client.get(url="/v1/groups/persons/", params=data)

    def get(self, id: int) -> Response:
        with self.get_client() as client:
            return client.get(url=f"/v1/groups/persons/{id}/")

    def update(self, id: int, name: str) -> Response:
        data = {"name": name}
        with self.get_client() as client:
            return client.patch(url=f"/v1/groups/persons/{id}/", json=data)

    def delete(self, id: int) -> Response:
        with self.get_client() as client:
            return client.delete(url=f"/v1/groups/persons/{id}/")

    def persons(
        self,
        id: int,
        pids: Union[List[str], object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self", "id"])

        with self.get_client() as client:
            return client.get(
                url=f"/v1/groups/persons/{id}/pids/", params=data
            )

    def add(self, pids: List[str], groups_ids: List[int]) -> Response:
        data = {"pids": pids, "groups_ids": groups_ids}
        with self.get_client() as client:
            return client.post(url="/v1/groups/persons/pids/", json=data)

    def remove(self, pids: List[str], groups_ids: List[int]) -> Response:
        data = {"pids": pids, "groups_ids": groups_ids}
        with self.get_client() as client:
            return client.request(
                "DELETE", url="/v1/groups/persons/pids/", json=data
            )


class GroupsAsync(APIBaseAsync):
    async def create(self, name: str) -> Response:
        data = {"name": name}
        async with self.get_client() as client:
            return await client.post(url="/v1/groups/persons/", json=data)

    async def list(
        self,
        q: Union[str, object] = sentinel,
        pids_include: Union[List[str], object] = sentinel,
        pids_exclude: Union[List[str], object] = sentinel,
        groups_ids: Union[List[int], object] = sentinel,
        spaces_ids: Union[List[int], object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self"])
        async with self.get_client() as client:
            return await client.get(url="/v1/groups/persons/", params=data)

    async def get(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.get(url=f"/v1/groups/persons/{id}/")

    async def update(self, id: int, name: str) -> Response:
        data = {"name": name}
        async with self.get_client() as client:
            return await client.patch(
                url=f"/v1/groups/persons/{id}/", json=data
            )

    async def delete(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.delete(url=f"/v1/groups/persons/{id}/")

    async def persons(
        self,
        id: int,
        pids: Union[List[str], object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self", "id"])
        async with self.get_client() as client:
            return await client.get(
                url=f"/v1/groups/persons/{id}/pids/", params=data
            )

    async def add(self, pids: List[str], groups_ids: List[int]) -> Response:
        data = {"pids": pids, "groups_ids": groups_ids}
        async with self.get_client() as client:
            return await client.post(url="/v1/groups/persons/pids/", json=data)

    async def remove(self, pids: List[str], groups_ids: List[int]) -> Response:
        data = {"pids": pids, "groups_ids": groups_ids}
        async with self.get_client() as client:
            return await client.request(
                "DELETE", url="/v1/groups/persons/pids/", json=data
            )
