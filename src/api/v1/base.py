from pydantic import BaseModel


class IDAMixin(BaseModel):
    id: str
