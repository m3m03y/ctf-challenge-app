"""Test flag validator module"""

import pytest
from ctf_server.core.flag_validator_strategy import (
    PlainInputPlainStoredValueStrategy,
    PlainInputStoredHashedStrategy,
    HashedInputHashedStoredValueStrategy,
)


class TestFlagValidatorStrategy:
    """Tests for different flag validator strategies"""

    @pytest.mark.parametrize(
        "flag, result",
        [
            ("flag{test_flag}", True),
            ("123", False),
            ("flag{abc_123_t1}", True),
            ("flag{#test}", False),
            ("flag(ttest)", False),
            ("flag{abc123}", True),
        ],
    )
    def test_flag_format_check_by_plain_input_strategies(
        self, flag: str, result: bool
    ) -> None:
        """Should properly check if flag is in format: flag{<a-z0-9_>} when plain input is taken"""
        strategy_1 = PlainInputPlainStoredValueStrategy()
        validation_result_1 = strategy_1.is_valid_format(flag) == result

        strategy_2 = PlainInputStoredHashedStrategy()
        validation_result_2 = strategy_2.is_valid_format(flag) == result

        assert validation_result_1 and validation_result_2

    @pytest.mark.parametrize(
        "flag, result",
        [
            ("d66b69a8e881ba6a0c6f4208ad425998", True),
            ("371def", True),
            ("ec1936de82200b89affbaae27305cf10", True),
            ("ah", False),
            ("ec1936de82200b89awwbaae27305cf10", False),
        ],
    )
    def test_flag_format_check_by_hashed_input_strategies(
        self, flag: str, result: bool
    ) -> None:
        """Should properly check whether flag is hexadecimal"""
        strategy = HashedInputHashedStoredValueStrategy()
        assert strategy.is_valid_format(flag) == result

    @pytest.mark.parametrize(
        "provided_flag, actual_flag, result",
        [
            ("flag{test_flag}", "flag{test_flag}", True),
            ("flag{other_flag}", "flag{test_value}", False),
            ("test", "test", True),
            ("test_value_1", "other_value", False),
        ],
    )
    def test_flags_should_be_equals_with_plain_input_plain_stored_value_strategy(
        self, provided_flag: str, actual_flag: str, result
    ) -> None:
        """
        Provided flag is equal to actual flag when both of them are the same text.
        There should be no additional checks. Same words should have same hashes.

        Args:
            provided_flag (str): flag in plain text
            actual_flag (str): stored flag in plain text
            result (_type_): when both plain text are equal should be True
        """
        strategy = PlainInputPlainStoredValueStrategy()
        assert (
            strategy.is_provided_flag_and_stored_value_equal(provided_flag, actual_flag)
            == result
        )

    @pytest.mark.parametrize(
        "provided_flag, stored_hash, result",
        [
            ("flag{test_flag}", "5aff3eee24f45a8f5a4c8e69c3a048b2", True),
            ("flag{other_flag}", "9c9989249fdd873d1d0a0119c00bfb79", False),
            ("test", "098f6bcd4621d373cade4e832627b4f6", True),
            ("test_value_1", "e6e412457f5ba622ccd5b77439a4746b", False),
        ],
    )
    def test_flag_hash_should_be_equal_to_stored_with_plain_input_hashed_stored_value_strategy(
        self, provided_flag: str, stored_hash: str, result
    ) -> None:
        """
        Provided flag is equal to actual flag when its hash is equal to stored hash.
        There should be no additional checks. Same words should have same hashes.

        Args:
            provided_flag (str): flag in plain text
            actual_flag (str): stored flag hash
            result (_type_): when both plain text are equal should be True
        """
        strategy = PlainInputStoredHashedStrategy()
        assert (
            strategy.is_provided_flag_and_stored_value_equal(provided_flag, stored_hash)
            == result
        )

    @pytest.mark.parametrize(
        "provided_flag, actual_flag, result",
        [
            (
                "5aff3eee24f45a8f5a4c8e69c3a048b2",
                "5aff3eee24f45a8f5a4c8e69c3a048b2",
                True,
            ),
            (
                "a6e203ab6b2a031032ffa6b26ce3ee19",
                "9c9989249fdd873d1d0a0119c00bfb79",
                False,
            ),
            (
                "098f6bcd4621d373cade4e832627b4f6",
                "098f6bcd4621d373cade4e832627b4f6",
                True,
            ),
            (
                "e2b77e665fb7a0ac55d41ec06885e2b0",
                "e6e412457f5ba622ccd5b77439a4746b",
                False,
            ),
        ],
    )
    def test_hashed_flag_and_stored_should_be_equal_with_hashed_input_hashed_stored_value_strategy(
        self, provided_flag: str, actual_flag: str, result
    ) -> None:
        """
        When provided flag is already hashed compare if it is equal to stored hash.
        There should be no additional checks. Same words should have same hashes.

        Args:
            provided_flag (str): flag in plain text
            actual_flag (str): stored flag hash
            result (_type_): when both plain text are equal should be True
        """
        strategy = HashedInputHashedStoredValueStrategy()
        assert (
            strategy.is_provided_flag_and_stored_value_equal(provided_flag, actual_flag)
            == result
        )
