from typing import Union

from src.models.base import IDAndConfigMixin


class Genre(IDAndConfigMixin):
    name: str
    description: Union[str, None] = None
