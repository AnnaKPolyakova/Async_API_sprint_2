import orjson
from pydantic import BaseModel

from models.utils import orjson_dumps


class IDAndConfigMixin(BaseModel):
    id: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
