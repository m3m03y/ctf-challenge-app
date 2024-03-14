"""Flag module"""

from pydantic import BaseModel


class Flag(BaseModel):
    """Class for keeping flag with challange"""

    value: str
    task_id: str
    challange_id: str
