'''Character generation endpoint'''
from typing import Any

from fastapi import APIRouter, HTTPException

from src import schemas
from src.generator.generation import generate_character, GenerationSetup
from src.generator.exceptions import NoDataForGeneration

router = APIRouter()


@router.post('/generate',
             response_model=schemas.GeneratedCharacter,
             responses={206: {'model': schemas.NoDataToGen}})
def gen_character(gen_request: schemas.GenerationRequest) -> Any:
    '''Generate the character'''

    setup = GenerationSetup(
        themes=gen_request.themes,
        gender=gen_request.gender,
        items=gen_request.n_items,
        n_positive_features=gen_request.n_positive_features,
        n_negative_features=gen_request.n_negative_features)
    try:
        return generate_character(setup)

    except NoDataForGeneration as exp:
        raise HTTPException(status_code=206, detail=str(exp))
