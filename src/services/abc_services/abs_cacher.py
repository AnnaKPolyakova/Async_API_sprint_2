from abc import ABC, abstractmethod
from typing import Optional


class ABSCacher(ABC):

    @abstractmethod
    async def put_by_id_to_cache(self, obj) -> None:
        pass

    @abstractmethod
    async def put_objs_to_cache(
            self,
            objs: list,
            size: int,
            page: int,
            sort: Optional[str],
            filter: Optional[str],
    ):
        pass

    @abstractmethod
    async def get_by_id_from_cache(self, obj_id: str):
        pass

    @abstractmethod
    async def get_objs_from_cache(
            self,
            size: int,
            page: int,
            sort: Optional[str],
            filter: Optional[str]
    ) -> list:
        pass

    @abstractmethod
    async def get_list_objects_cache_key(*args) -> str:
        pass
