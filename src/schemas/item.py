'''Schemas for API responses'''

from pydantic import BaseModel


class ItemModel(BaseModel):
    '''Feature response schema'''
    id: int
    name: str
    description: str
