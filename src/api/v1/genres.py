from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, Query

from api.v1.models_schems import Genre
from core.config import settings
from services.objects_finder import ObjectsFinder
from services.services import get_genre_service

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


@router.get("/", response_model=List[Genre])
async def genre_list(
    size: int = Query(
        default=settings["SIZE"],
        title="Genres numbers per page",
        ge=0
    ),
    page: int = Query(1, description="Page number", ge=0),
    sort: Union[str, None] = Query(
        None, description="Sorting fields (Example: name:desc)"),
    filter: Union[str, None] = Query(
        None, description="Filter by genre id (Example: name::Wyclef Jean)"
    ),
    genre_service: ObjectsFinder = Depends(get_genre_service),
) -> List[Genre]:
    genres = await genre_service.get_objs_list(size, page, sort, filter)
    return [Genre(**genre.dict(by_alias=True)) for genre in genres]
