"""Flag endpoints"""

import fastapi
from fastapi import Response, status
from ctf_server.model.flag import Flag
from ctf_server.model.state import State
from ctf_server.db.azure_proxy import AzureProxy
from ctf_server.core.flag_validator_strategy import PlainInputStoredHashedStrategy
from ctf_server.service.flag_service import FlagService

router = fastapi.APIRouter()
flag_service = FlagService(AzureProxy(), PlainInputStoredHashedStrategy())


@router.post("/submit-flag", status_code=status.HTTP_200_OK)
async def submit_flag(flag: Flag, response: Response) -> dict:
    """Handles flag submit"""
    state = flag_service.submit_flag(flag)
    if state in (State.INVALID_FORMAT, State.INVALID_FLAG):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"stage": state}

    next_task = flag_service.get_next_task(flag.challenge_id, flag.task_nr)
    return {"state": state, "task_nr": next_task}


@router.post("/flag", status_code=status.HTTP_201_CREATED)
async def create_flag(flag: Flag, response: Response) -> dict:
    """Handles flag create"""

    flag = flag_service.create_flag(flag)
    if flag is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return {"error": "CREATE_FAILED"} if flag is None else {"flag": flag}


@router.get("/flag/", status_code=status.HTTP_200_OK)
async def get_flag(challenge_id: str, task_id: str) -> dict:
    """Handles flag get request"""
    flag = flag_service.get_flag(challenge_id, task_id)
    return {"flag": flag}


@router.get("/flag", status_code=status.HTTP_200_OK)
async def get_all_flags() -> dict:
    """Handles flag submit"""
    flags = flag_service.get_all_flags()
    return {"flags": flags}


@router.put("/flag", status_code=status.HTTP_200_OK)
async def update_flag(flag: Flag) -> dict:
    """Handles flag update"""
    flag = flag_service.update_flag(flag)
    return {"error": "UPDATE_FAILED"} if flag is None else {"flag": flag}


@router.delete("/flag/", status_code=status.HTTP_200_OK)
async def delete_flag(challenge_id: str, task_id: str) -> dict:
    """Handles flag delete"""
    is_deleted = flag_service.remove_flag(challenge_id, task_id)
    return {"is_deleted": is_deleted}
