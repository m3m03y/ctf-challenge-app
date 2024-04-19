"""Flag module"""

from ctf_server.db.dto.flag_dto import FlagDto
from pydantic import BaseModel


class Flag(BaseModel):
    """Class for keeping flag with challenge"""

    value: str
    task_id: str
    challenge_id: str
    task_nr: int

    @classmethod
    def from_dto(cls, dto_obj: FlagDto):
        """Convert dto to Flag object"""
        return cls(
            value=dto_obj.value,
            challenge_id=dto_obj.challenge_id,
            task_id=dto_obj.task_id,
            task_nr=dto_obj.task_nr,
        )
