from http import HTTPStatus
from typing import Optional
from fastapi import Request

from fastapi import APIRouter, Depends, HTTPException, Query

from src.api.v1.models_schems import Genre
from src.core.config import settings
from src.services.objects_finder import ObjectsFinder
from src.services.services import get_genre_service
from src.services.utils import authentication_required

router = APIRouter()


@router.get("/{genre_id}", response_model=Genre)
async def genre_details(
    genre_id: str, genre_service: ObjectsFinder = Depends(get_genre_service)
) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="genre not found"
        )
    enre_dict = genre.dict()
    return enre_dict


@router.get("/", response_model=list[Genre])
@authentication_required
async def genre_list(
    request: Request,
    size: int = Query(
        default=settings.SIZE,
        title="Genres numbers per page",
        ge=0
    ),
    page: int = Query(1, description="Page number", ge=0),
    sort: Optional[str] = Query(
        None, description="Sorting fields (Example: name:desc)"),
    filter: Optional[str] = Query(
        None, description="Filter by genre id (Example: name::Wyclef Jean)"
    ),
    genre_service: ObjectsFinder = Depends(get_genre_service),
) -> list[Genre]:
    genres = await genre_service.get_objs_list(size, page, sort, filter)
    return [Genre(**genre.dict(by_alias=True)) for genre in genres]
