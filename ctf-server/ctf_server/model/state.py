"""State module"""

from enum import Enum


class State(str, Enum):
    """Class for keeping flag with challenge"""

    INVALID_FORMAT = "INVALID_FORMAT"
    INVALID_FLAG = "INVALID_FLAG"
    VALID_FLAG = "VALID_FLAG"
