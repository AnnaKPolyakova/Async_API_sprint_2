from abc import ABC, abstractmethod
from typing import List, Optional, Union

from pydantic import BaseModel


class ABSSearcher(ABC):

    @abstractmethod
    async def get_obj_from_elastic(self, obj_id: str) -> Optional[BaseModel]:
        pass

    @abstractmethod
    async def get_objs_from_elastic(
            self,
            size: int,
            page: int,
            sort: Union[str, None],
            filter: Union[str, None]
    ) -> List[BaseModel]:
        pass
