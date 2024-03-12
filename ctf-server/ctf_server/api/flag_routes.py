"""Flag endpoints"""

import fastapi
from fastapi import Response, status
from ctf_server.model.flag import Flag
from ctf_server.model.state import State
from ctf_server.db.azure_proxy import AzureProxy
from ctf_server.core.flag_validator_strategy import PlainInputPlainStoredValueStrategy
from ctf_server.service.flag_service import FlagService

router = fastapi.APIRouter()
flag_service = FlagService(AzureProxy(), PlainInputPlainStoredValueStrategy())

@router.post("/submit-flag", status_code=status.HTTP_200_OK)
async def submit_flag(flag: Flag, response: Response) -> dict:
    """Handles flag submit"""
    state = flag_service.submit_flag(flag)
    if state in (State.INVALID_FORMAT, State.INVALID_FLAG):
        response.status_code = status.HTTP_400_BAD_REQUEST
    return {"state": state}

@router.post("/flag", status_code=status.HTTP_201_CREATED)
async def create_flag(flag: Flag, response: Response) -> dict:
    """Handles flag create"""

    flag = flag_service.create_flag(flag)
    if flag is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return {"flag": flag}

@router.get("/flag/", status_code=status.HTTP_200_OK)
async def get_flag(challange_id: str, task_id: str) -> dict:
    """Handles flag get request"""
    flag = flag_service.get_flag(challange_id, task_id)
    return {"flag": flag}

@router.get("/flag", status_code=status.HTTP_200_OK)
async def get_all_flags() -> dict:
    """Handles flag submit"""
    flags = flag_service.get_all_flags()
    return {"flags": flags}
