from datetime import datetime
from typing import List, Union

from httpx import Response

from neuroio.api.base import APIBase, APIBaseAsync
from neuroio.constants import EntryLiveness, EntryMood, EntryResult, sentinel
from neuroio.utils import request_query_processing


class Entries(APIBase):
    def list(
        self,
        pid: Union[List[str], object] = sentinel,
        result: Union[List[EntryResult], object] = sentinel,
        age_from: Union[int, object] = sentinel,
        age_to: Union[int, object] = sentinel,
        sex: Union[int, object] = sentinel,
        mood: Union[List[EntryMood], object] = sentinel,
        liveness: Union[List[EntryLiveness], object] = sentinel,
        sources_ids: Union[List[int], object] = sentinel,
        spaces_ids: Union[List[int], object] = sentinel,
        date_from: Union[datetime, object] = sentinel,
        date_to: Union[datetime, object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self"])
        with self.get_client() as client:
            return client.get(url="/v1/entries/", params=data)

    def get(self, pid: str) -> Response:
        with self.get_client() as client:
            return client.get(url=f"/v1/entries/stats/pid/{pid}/")

    def delete(self, pid: str) -> Response:
        with self.get_client() as client:
            return client.delete(url=f"/v1/entries/{pid}/")


class EntriesAsync(APIBaseAsync):
    async def list(
        self,
        pid: Union[List[str], object] = sentinel,
        result: Union[List[EntryResult], object] = sentinel,
        age_from: Union[int, object] = sentinel,
        age_to: Union[int, object] = sentinel,
        sex: Union[int, object] = sentinel,
        mood: Union[List[EntryMood], object] = sentinel,
        liveness: Union[List[EntryLiveness], object] = sentinel,
        sources_ids: Union[List[int], object] = sentinel,
        spaces_ids: Union[List[int], object] = sentinel,
        date_from: Union[datetime, object] = sentinel,
        date_to: Union[datetime, object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self"])
        async with self.get_client() as client:
            return await client.get(url="/v1/entries/", params=data)

    async def get(self, pid: str) -> Response:
        async with self.get_client() as client:
            return await client.get(url=f"/v1/entries/stats/pid/{pid}/")

    async def delete(self, pid: str) -> Response:
        async with self.get_client() as client:
            return await client.delete(url=f"/v1/entries/{pid}/")
