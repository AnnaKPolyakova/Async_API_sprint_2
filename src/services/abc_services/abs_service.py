from abc import ABC, abstractmethod
from typing import List, Optional, Union

from pydantic import BaseModel


class ABSObjectsFinder(ABC):

    @abstractmethod
    async def get_by_id(self, film_id: str) -> Optional[BaseModel]:
        pass

    @abstractmethod
    async def get_objs_list(
            self,
            size: int,
            page: int,
            sort: Union[str, None],
            filter: Union[str, None]
    ) -> Optional[List[BaseModel]]:
        pass
