"""Flag Validator module"""

from __future__ import annotations
import re
import logging
from enum import Flag
from ctf_server.core.flag_validator_strategy import FlagValidatorStrategy
from ctf_server.model.state import State

_FLAG_FORMAT = r"^flag\{[a-z0-9_]*\}"


class FlagValidator:
    """Validates flags provided by user using md5"""

    def __init__(self, strategy: FlagValidatorStrategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> FlagValidatorStrategy:
        """Current used strategy"""
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: FlagValidatorStrategy) -> None:
        self._strategy = strategy

    def validate_flag_format(self, flag: str) -> bool:
        """Check whether flag matches valid pattern: flag{hidden_text}

        Args:
            flag (str): flag word provided by user

        Returns:
            bool: true if flag matches format
        """
        # flag_pattern = re.compile(_FLAG_FORMAT)
        return re.fullmatch(_FLAG_FORMAT, flag)

    def is_valid_flag(self, flag: Flag) -> State:
        """
        Check whether provided by user flag is valid:
        - is in correct format
        - matches stored value

        Args:
            flag (Flag): flag word provided by user

        Returns:
            State: validation state
        """
        is_valid = self.validate_flag_format(flag.value)
        if not is_valid:
            logging.debug("FLAG_VALIDATOR::Provided flag with invalid format: %s", flag)
            return State.INVALID_FORMAT
        is_valid = self.strategy.is_provided_flag_and_stored_value_equal(
            flag.value, "flag{test}"
        )
        logging.debug("FLAG_VALIDATOR::Provided flag: %s", flag)
        return State.VALID_FLAG if is_valid else State.INVALID_FLAG
