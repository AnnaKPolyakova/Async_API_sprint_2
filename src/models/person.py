from typing import Optional

from src.models.base import IDAndConfigMixin


class Person(IDAndConfigMixin):
    full_name: str
    gender: Optional[str] = None
