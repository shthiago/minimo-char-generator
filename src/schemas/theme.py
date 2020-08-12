'''Schemas for API responses'''

from pydantic import BaseModel


class ThemeModel(BaseModel):
    '''Name response schema'''

    id: int
    name: str
