"""Flag validation stratiegies"""

import re
from abc import ABC, abstractmethod
from ctf_server.core.crypto import Crypto

_FLAG_FORMAT = r"^flag\{[a-z0-9_]*\}"


class FlagValidatorStrategy(ABC):
    """Declares operation for comparision of user input and stored value"""

    @abstractmethod
    def is_provided_flag_and_stored_value_equal(
        self, user_input: str, stored_value: str
    ) -> bool:
        """Compare user input and stored value, based on specific rules"""

    def is_valid_format(self, flag: str) -> bool:
        """Check whether flag provided by user matches valid format"""
        return re.fullmatch(_FLAG_FORMAT, flag)


class PlainInputStoredHashedStrategy(FlagValidatorStrategy):
    """Handles comparision when user input is plain text and stored value is md5 hash"""

    def is_provided_flag_and_stored_value_equal(
        self, user_input: str, stored_value: str
    ) -> bool:
        return Crypto.compare_word_with_hash(user_input, stored_value)


class PlainInputPlainStoredValueStrategy(FlagValidatorStrategy):
    """
    Handles comparision when both user input and stored value are plain text
    Default strategy.
    """

    def is_provided_flag_and_stored_value_equal(
        self, user_input: str, stored_value: str
    ) -> bool:
        return Crypto.compare_word_hashes(user_input, stored_value)


class HashedInputHashedStoredValueStratedy(FlagValidatorStrategy):
    """Handles comparision when both user input and stored value are md5 hash"""

    def is_provided_flag_and_stored_value_equal(
        self, user_input: str, stored_value: str
    ) -> bool:
        return user_input == stored_value

    def is_valid_format(self, flag: str) -> bool:
        try:
            int(flag, 16)
            return True
        except ValueError:
            return False
