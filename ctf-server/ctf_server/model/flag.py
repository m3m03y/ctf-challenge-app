"""Flag module"""

from pydantic import BaseModel


class Flag(BaseModel):
    """Class for keeping flag with challange"""

    value: str
    task: int = 0
