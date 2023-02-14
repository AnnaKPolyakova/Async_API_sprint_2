from typing import Optional

from src.models.base import IDAndConfigMixin


class Genre(IDAndConfigMixin):
    name: str
    description: Optional[str] = None
