'''Schemas for API responses'''

from pydantic import BaseModel


class NameModel(BaseModel):
    '''Name response schema'''

    id: int
    firstname: str
    lastname: str
    gender: str
