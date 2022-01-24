from abc import ABC, abstractmethod


class AsyncSearchEngin(ABC):
    @abstractmethod
    async def get(self, index: str, instance_id: str, **kwargs):
        pass

    @abstractmethod
    async def search(self, index: str, query_: dict, **kwargs):
        pass
