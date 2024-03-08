"""Flag validation stratiegies"""

from abc import ABC, abstractmethod

from ctf_server.core.crypto import Crypto


class FlagValidatorStrategy(ABC):
    """Declares operation for comparision of user input and stored value"""

    @abstractmethod
    def is_provided_flag_and_stored_value_equal(
        self, user_input: str, stored_value: str
    ) -> bool:
        """
        Abstract method to implement specific comparision of user
        input and stored value
        """


class PlainInputStoredHashedStrategy(FlagValidatorStrategy):
    """Handles comparision when user input is plain text and stored value is md5 hash"""

    def is_provided_flag_and_stored_value_equal(
        self, user_input: str, stored_value: str
    ) -> bool:
        return Crypto.compare_word_with_hash(user_input, stored_value)


class PlainInputPlainStoredValueStrategy(FlagValidatorStrategy):
    """Handles comparision when both user input and stored value are plain text"""

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
