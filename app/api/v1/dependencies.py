from fastapi import Depends
from typing import Annotated

from app.schemas.filters import FilteringParams
from app.utils.filters import get_filtering_params
from app.utils.unitofwork import IUnitOfWork, UnitOfWork
from app.utils.auth import get_current_user

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
CurrentUser = Annotated[str, Depends(get_current_user)]
FilteringDep = Annotated[FilteringParams, Depends(get_filtering_params)]

