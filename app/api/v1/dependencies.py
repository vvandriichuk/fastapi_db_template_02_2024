from fastapi import Depends
from typing import Annotated

from utils.unitofwork import IUnitOfWork, UnitOfWork
from utils.auth import get_current_user

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
CurrentUser = Annotated[str, Depends(get_current_user)]
