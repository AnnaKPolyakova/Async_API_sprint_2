from typing import Dict, List, Union
from api.v1.base import IDAMixin


class Film(IDAMixin):
    title: str
    imdb_rating: float
    description: Union[str, None] = None
    genre: List[str]
    director: List[str]
    writers: Union[List[Dict], None] = None
    writers_names: Union[List[str], None] = None
    actors: Union[List[Dict], None] = None
    actors_names: Union[List[str], None] = None


class FilmList(IDAMixin):
    title: str
    imdb_rating: float
    description: Union[str, None] = None


class Genre(IDAMixin):
    name: str
    description: Union[str, None] = None


class Person(IDAMixin):
    full_name: str
    gender: Union[str, None] = None
