import abc

from httpx import AsyncClient, Client


class APIBase(abc.ABC):
    def __init__(self, settings: dict) -> None:
        self.settings = settings

    def get_client(self) -> Client:
        return Client(**self.settings)


class APIBaseAsync(abc.ABC):
    def __init__(self, settings: dict) -> None:
        self.settings = settings

    def get_client(self) -> AsyncClient:
        return AsyncClient(**self.settings)
