"""Flag module"""

from pydantic import BaseModel


class Flag(BaseModel):
    """Class for keeping flag with challenge"""

    value: str
    task_id: str
    challenge_id: str
    task_nr: int
