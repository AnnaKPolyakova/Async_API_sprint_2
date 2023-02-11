from typing import Dict, List, Union

from src.models.base import IDAndConfigMixin


class Film(IDAndConfigMixin):
    title: str
    imdb_rating: float
    description: Union[str, None] = None
    genre: List[str]
    director: List[str]
    writers: Union[List[Dict], None] = None
    writers_names: Union[List[str], None] = None
    actors: Union[List[Dict], None] = None
    actors_names: Union[List[str], None] = None
