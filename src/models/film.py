from typing import Optional

from src.models.base import IDAndConfigMixin


class Film(IDAndConfigMixin):
    title: str
    imdb_rating: float
    description: Optional[str] = None
    genre: list[str]
    director: list[str]
    writers: Optional[list[dict]] = None
    writers_names: Optional[list[str]] = None
    actors: Optional[list[dict]] = None
    actors_names: Optional[list[str]] = None
