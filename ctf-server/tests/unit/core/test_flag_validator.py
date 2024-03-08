"""Test flag validator module"""

import pytest
from ctf_server.core.flag_validator import FlagValidator


class TestFlagValidator:
    """Tests for flag validator functions"""

    flag_validator: FlagValidator = FlagValidator()

    @pytest.mark.parametrize(
        "flag",
        [
            ("flag{test_123}"),
            ("flag{test}"),
            ("flag{t}"),
            ("flag{test_123_asd}"),
            ("flag{5361}"),
        ],
    )
    def test_should_match_flag_format(self, flag: str) -> None:
        """Test flag format check when flag in valid provided"""
        assert self.flag_validator.validate_flag_format(flag)

    @pytest.mark.parametrize(
        "flag",
        [
            ("flag{test-123}"),
            ("{test}"),
            ("flag{t#@!}"),
            ("flag{test-123_asd}"),
            ("5361"),
            ("test"),
            ("test{1231251_123ad}"),
            ("flag{#$}"),
            ("flag{Contains_upper_letters}"),
        ],
    )
    def test_should_not_match_flag_format(self, flag: str) -> None:
        """Test flag format check when flag in wrong format provided"""
        assert not self.flag_validator.validate_flag_format(flag)
