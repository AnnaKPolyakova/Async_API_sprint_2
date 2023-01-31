from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from api.v1.models_schems import Film, FilmList
from core.config import settings
from services.objects_finder import ObjectsFinder
from services.services import get_film_service

router = APIRouter()


@router.get("/{film_id}", response_model=Film)
async def film_details(
    film_id: str, film_service: ObjectsFinder = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="film not found"
        )
    film_dict = film.dict()
    return film_dict


@router.get("/", response_model=List[FilmList])
async def film_list(
    size: int = Query(
        default=settings["SIZE"], title="Films numbers per page", ge=0
    ),
    page: int = Query(default=1, title="Page number", ge=0),
    sort: str = Query(
        None,
        description="Sorting fields ("
        "Examples: imdb_rating:desc, itle.keyword:asc"
        ")",
    ),
    filter: str = Query(
        None, description="Filter by genre id (Example: title::Wyclef Jean)"
    ),
    film_service: ObjectsFinder = Depends(get_film_service),
) -> List[Film]:
    films = await film_service.get_objs_list(size, page, sort, filter)
    return [FilmList(**film.dict(by_alias=True)) for film in films]
