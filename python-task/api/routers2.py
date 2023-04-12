from fastapi import (
    APIRouter,
    Depends
)
from typing import List

from db.schema import (
    PriorityCode,
    PriorityCodeModel
)
from api.exceptions.model import UnexpectedDatabaseError
from api.auth import is_authenticated


API2 = APIRouter()


@API2.get(
    path="/",
    response_model=List[PriorityCodeModel],
    description='Returns a list of all possible priority codes',
    dependencies=[Depends(is_authenticated)]
)
async def get_all_codes() -> List[PriorityCodeModel]:
    try:        
        return await PriorityCodeModel.from_queryset(PriorityCode.all())
    except Exception as e:
        raise UnexpectedDatabaseError(str(e))


@API2.get(
    path="/{priorityCode}",
    response_model=int,
    description='Returns 1 if priority code exists, otherwise returns 0',
    dependencies=[Depends(is_authenticated)]
)
async def code_exists(priorityCode: str) -> int:
    try:        
        code = await PriorityCode.filter(code=priorityCode)
        return 1 if len(code) > 0 else 0
    except Exception as e:
        raise UnexpectedDatabaseError(str(e))