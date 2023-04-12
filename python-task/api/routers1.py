from fastapi import (
    APIRouter,
    Depends
)
from typing import List

from db.schema import (
    CountryModel,
    Country
)
from api.exceptions.model import UnexpectedDatabaseError
from api.auth import is_authenticated


API1 = APIRouter(prefix='/MasterData')


@API1.get(
    path="/Country",
    response_model=List[CountryModel],
    description='Returns a list of countries. Country properties: code, name, description, region.',
    dependencies=[Depends(is_authenticated)]
)
async def get_country_data(countryName: str = None) -> List[CountryModel]:
    try:
        if countryName is not None:
            return await CountryModel.from_queryset(Country.filter(name=countryName))
        
        return await CountryModel.from_queryset(Country.all())
    except Exception as e:
        raise UnexpectedDatabaseError(str(e))
