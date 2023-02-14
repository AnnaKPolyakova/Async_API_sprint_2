from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel


class ABSObjectsFinder(ABC):

    @abstractmethod
    async def get_by_id(self, obj_id: str) -> Optional[BaseModel]:
        pass

    @abstractmethod
    async def get_objs_list(
            self,
            size: int,
            page: int,
            sort: Optional[str],
            filter: Optional[str]
    ) -> Optional[list[BaseModel]]:
        pass
