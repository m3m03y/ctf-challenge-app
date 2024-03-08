"""Flag endpoints"""

import logging
import fastapi
from fastapi import Response, status
from ctf_server.model.flag import Flag
from ctf_server.model.state import State
from ctf_server.core.flag_validator import FlagValidator

router = fastapi.APIRouter()


@router.post("/flag", status_code=200)
async def submit_flag(flag: Flag, response: Response) -> dict:
    """Handles flag submit"""
    is_valid = FlagValidator.validate_flag_format(flag.value)
    if not is_valid:
        response.status_code = status.HTTP_201_CREATED
        logging.debug("SUBMIT_FLAG::Provided flag with invalid format: %s", flag)
        return {"state": State.INVALID_FORMAT}
    is_valid = FlagValidator.compare_word_hashes(flag.value, "flag{test}")
    logging.debug("SUBMIT_FLAG::Provided flag: %s", flag)
    return {"state": State.VALID_FLAG} if is_valid else {"state": State.INVALID_FLAG}
