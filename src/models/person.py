from typing import Union

from src.models.base import IDAndConfigMixin


class Person(IDAndConfigMixin):
    full_name: str
    gender: Union[str, None] = None
