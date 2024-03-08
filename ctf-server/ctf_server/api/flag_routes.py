"""Flag endpoints"""

import fastapi
from fastapi import Response, status
from ctf_server.model.flag import Flag
from ctf_server.model.state import State
from ctf_server.core.flag_validator import FlagValidator
from ctf_server.core.flag_validator_strategy import PlainInputPlainStoredValueStrategy

router = fastapi.APIRouter()


@router.post("/flag", status_code=status.HTTP_200_OK)
async def submit_flag(flag: Flag, response: Response) -> dict:
    """Handles flag submit"""
    flag_validator = FlagValidator(PlainInputPlainStoredValueStrategy())
    state = flag_validator.is_valid_flag(flag)
    if state in (State.INVALID_FORMAT, State.INVALID_FLAG):
        response.status_code = status.HTTP_400_BAD_REQUEST
    return {"state": state}
