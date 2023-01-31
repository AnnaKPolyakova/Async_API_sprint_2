from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from api.v1.models_schems import Person
from core.config import settings
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get("/{person_id}", response_model=Person)
async def person_details(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="person not found"
        )
    enre_dict = person.dict()
    return enre_dict


@router.get("/", response_model=List[Person])
async def person_list(
    size: int = Query(
        settings["SIZE"], description="Films numbers per page", ge=0
    ),
    page: int = Query(1, description="Page number", ge=0),
    sort: str = Query(
        None, description="Sorting fields (Example: full_name:desc)"
    ),
    filter: str = Query(
        None,
        description="Filter by person id (Example: full_name::Wyclef Jean)"
    ),
    person_service: PersonService = Depends(get_person_service),
) -> List[Person]:
    persons = await person_service.get_persons_list(size, page, sort, filter)
    return [Person(**person.dict(by_alias=True)) for person in persons]
