"""Test flag validator module"""

import pytest
from ctf_server.model.state import State
from ctf_server.core.flag_validator import FlagValidator
from ctf_server.core.flag_validator_strategy import (
    PlainInputPlainStoredValueStrategy,
)


class TestFlagValidator:
    """Tests for flag validator functions"""

    flag_validator: FlagValidator = FlagValidator()

    @pytest.mark.parametrize(
        "flag",
        [
            ("flag{f}"),
            ("flag{_}"),
            ("flag{1}"),
            ("flag{flag}"),
            ("flag{flag_}"),
            ("flag{flag1}"),
            ("flag{flag_1}"),
            ("flag{multiple_words_flag}"),
        ],
    )
    def test_should_match_flag_format(self, flag: str) -> None:
        """Test flag format check when flag in valid provided"""
        assert self.flag_validator.validate_flag_format(flag)

    @pytest.mark.parametrize(
        "flag",
        [
            ("flag{}"),
            ("flag{-}"),
            ("flag{#}"),
            ("flag{Flag}"),
            ("no_flag"),
            (""),
            ("flag{flag!}"),
        ],
    )
    def test_should_not_match_flag_format(self, flag: str) -> None:
        """Test flag format check when flag in wrong format provided"""
        assert not self.flag_validator.validate_flag_format(flag)

    @pytest.mark.parametrize(
        "flag, actual_flag, result",
        [
            ("abc", "flag{valid}", State.INVALID_FORMAT),
            ("flag{test_with_wrong_signs_#}", "flag{valid}", State.INVALID_FORMAT),
            ("flag{Valid}", "flag{valid}", State.INVALID_FORMAT),
            ("flag{test_flag}", "flag{other_flag}", State.INVALID_FLAG),
            ("flag{t3st_fl4g}", "flag{test_flag}", State.INVALID_FLAG),
            ("flag{valid_flag}", "flag{valid_flag}", State.VALID_FLAG)
        ],
    )
    def test_provided_flag_with_same_value_as_actual_flag_should_be_valid(
        self, flag: str, actual_flag: str, result: State
    ) -> None:
        """
        Test PlainInputPlainStoredValueStrategy, given provided flag is
        equal to actual flag then both hashes of these flags should be
        equal

        Args:
            flag (str): flag provided by user_
            actual_flag (str): stored value of flag for specific exercise
            result (bool): true when both values are plain text and their
            hashes are equal
        """
        self.flag_validator.strategy = PlainInputPlainStoredValueStrategy()
        assert self.flag_validator.is_valid_flag(flag, actual_flag) == result
