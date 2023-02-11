from typing import Optional, Union

from src.models.film import Film
from src.services.abc_services.abs_casher import ABSCasher
from src.services.abc_services.abs_searcher import ABSSearcher
from src.services.abc_services.abs_service import ABSObjectsFinder


class ObjectsFinder(ABSObjectsFinder):
    def __init__(
            self,
            casher: ABSCasher,
            searcher: ABSSearcher
    ):
        self.casher = casher
        self.searcher = searcher

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self.casher.get_by_id_from_cache(film_id)
        if not film:
            film = await self.searcher.get_obj_from_elastic(film_id)
            if not film:
                return None
            await self.casher.put_by_id_to_cache(film)
        return film

    async def get_objs_list(
            self,
            size: int,
            page: int,
            sort: Union[str, None],
            filter: Union[str, None]
    ) -> Optional[Film]:
        films = await self.casher.get_objs_from_cache(size, page, sort, filter)
        if not films:
            films = await self.searcher.get_objs_from_elastic(
                size, page, sort, filter
            )
            await self.casher.put_objs_to_cache(
                films, size, page, sort, filter
            )
        return films
