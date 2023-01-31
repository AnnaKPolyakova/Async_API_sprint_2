from abc import ABC, abstractmethod
from typing import List, Union


class ABSCasher(ABC):

    @abstractmethod
    async def put_by_id_to_cache(self, obj) -> None:
        pass

    @abstractmethod
    async def put_objs_to_cache(
            self,
            objs: List,
            size: int,
            page: int,
            sort: Union[str, None],
            filter: Union[str, None],
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
            sort: Union[str, None],
            filter: Union[str, None]
    ) -> List:
        pass

    @abstractmethod
    async def get_list_objects_cache_key(*args) -> str:
        pass
