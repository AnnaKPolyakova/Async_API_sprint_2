from typing import Optional

from src.api.v1.base import IDAMixin


class Film(IDAMixin):
    title: str
    imdb_rating: float
    description: Optional[str] = None
    genre: list[str]
    director: list[str]
    writers: Optional[list[dict]] = None
    writers_names: Optional[list[str]] = None
    actors: Optional[list[dict]] = None
    actors_names: Optional[list[str]] = None


class FilmList(IDAMixin):
    title: str
    imdb_rating: float
    description: Optional[str] = None


class Genre(IDAMixin):
    name: str
    description: Optional[str] = None


class Person(IDAMixin):
    full_name: str
    gender: Optional[str] = None
