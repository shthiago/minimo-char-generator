'''Schemas for API responses'''

from pydantic import BaseModel


class FeatureModel(BaseModel):
    '''Feature response schema'''
    id: int
    text_masc: str
    text_fem: str
    description: str
    is_good: bool
