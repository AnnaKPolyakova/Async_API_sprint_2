from http import HTTPStatus
from fastapi import Request

from fastapi import APIRouter, Depends, HTTPException, Query

from src.api.v1.models_schems import Film, FilmList
from src.core.config import settings
from src.services.objects_finder import ObjectsFinder
from src.services.services import get_film_service
from src.services.utils import authentication_required

router = APIRouter()


@router.get("/{film_id}", response_model=Film)
@authentication_required
async def film_details(
        request: Request,
        film_id: str, film_service: ObjectsFinder = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="film not found"
        )
    film_dict = film.dict()
    return film_dict


@router.get("/", response_model=list[FilmList])
@authentication_required
async def film_list(
    request: Request,
    size: int = Query(
        default=settings.SIZE, title="Films numbers per page", ge=0
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
) -> list[Film]:
    films = await film_service.get_objs_list(size, page, sort, filter)
    return [FilmList(**film.dict(by_alias=True)) for film in films]
