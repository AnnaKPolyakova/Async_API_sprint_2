from typing import Optional

from src.models.film import Film
from src.services.abc_services.abs_cacher import ABSCacher
from src.services.abc_services.abs_searcher import ABSSearcher
from src.services.abc_services.abs_service import ABSObjectsFinder


class ObjectsFinder(ABSObjectsFinder):
    def __init__(
            self,
            cacher: ABSCacher,
            searcher: ABSSearcher
    ):
        self.cacher = cacher
        self.searcher = searcher

    async def get_by_id(self, obj_id: str) -> Optional[Film]:
        film = await self.cacher.get_by_id_from_cache(obj_id)
        if not film:
            film = await self.searcher.get_obj_from_elastic(obj_id)
            if not film:
                return None
            await self.cacher.put_by_id_to_cache(film)
        return film

    async def get_objs_list(
            self,
            size: int,
            page: int,
            sort: Optional[str],
            filter: Optional[str]
    ) -> Optional[Film]:
        films = await self.cacher.get_objs_from_cache(size, page, sort, filter)
        if not films:
            films = await self.searcher.get_objs_from_elastic(
                size, page, sort, filter
            )
            await self.cacher.put_objs_to_cache(
                films, size, page, sort, filter
            )
        return films
