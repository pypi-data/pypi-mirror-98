from typing.io import BinaryIO

from httpx import Response

from neuroio.api.base import APIBase, APIBaseAsync
from neuroio.constants import EntryResult


class Utility(APIBase):
    def compare(
        self, image1: BinaryIO, image2: BinaryIO, result: str = EntryResult.HA
    ) -> Response:
        files = {"image1": image1, "image2": image2}
        data = {"result": result}

        with self.get_client() as client:
            return client.post(
                url="/v1/utility/compare/", data=data, files=files
            )

    def asm(self, image: BinaryIO) -> Response:
        files = {"image": image}

        with self.get_client() as client:
            return client.post(url="/v1/utility/asm/", files=files)


class UtilityAsync(APIBaseAsync):
    async def compare(
        self, image1: BinaryIO, image2: BinaryIO, result: str = EntryResult.HA
    ) -> Response:
        files = {"image1": image1, "image2": image2}
        data = {"result": result}

        async with self.get_client() as client:
            return await client.post(
                url="/v1/utility/compare/", data=data, files=files
            )

    async def asm(self, image: BinaryIO) -> Response:
        files = {"image": image}

        async with self.get_client() as client:
            return await client.post(url="/v1/utility/asm/", files=files)
