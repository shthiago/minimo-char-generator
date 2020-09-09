'''Schemas for API generation response/request'''
from typing import List, Optional, Tuple

from pydantic import BaseModel

from src.schemas.name import NameModel
from src.schemas.item import ItemModel
from src.schemas.feature import FeatureModel


class GeneratedCharacter(BaseModel):
    '''Generated Charactere structure'''
    name: NameModel
    positive_features: List[FeatureModel]
    negative_features: List[FeatureModel]
    items: List[ItemModel]


class GenerationRequest(BaseModel):
    '''Fields for generation a character'''
    themes: Optional[Tuple[str, ...]] = None
    gender: str = 'any'
    n_positive_features: int = 5
    n_negative_features: int = 3
    n_items: int = 3


class NoDataToGen(BaseModel):
    '''Response to when no character was generated'''
    detail: str
