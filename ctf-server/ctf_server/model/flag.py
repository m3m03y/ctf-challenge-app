"""Flag module"""

from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class Flag(BaseModel):
    """Class for keeping flag with challange"""

    value: str
    task: int = 0
