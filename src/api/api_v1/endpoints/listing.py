'''Endpoints for listing items on database'''

from typing import Any, List

from fastapi import APIRouter

from src.database.dao import FeatureDAO, NameDAO, ItemDAO, ThemeDAO
from src import schemas

router = APIRouter()


@router.get('/listing/items', response_model=List[schemas.ItemModel])
def list_all_items() -> Any:
    '''Return all items on database'''
    dao = ItemDAO()

    return dao.list_all()


@router.get('/listing/features', response_model=List[schemas.FeatureModel])
def list_all_features() -> Any:
    '''Return all features on database'''
    dao = FeatureDAO()

    return dao.list_all()


@router.get('/listing/themes', response_model=List[schemas.ThemeModel])
def list_all_themes() -> Any:
    '''Return all themes on database'''
    dao = ThemeDAO()

    return dao.list_all()


@router.get('/listing/names', response_model=List[schemas.NameModel])
def list_all_names() -> Any:
    '''Return all Names on database'''
    dao = NameDAO()

    return dao.list_all()
