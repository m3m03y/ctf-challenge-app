"""Test flag validator module"""
import pytest
from ctf_server.core.flag_validator import FlagValidator

class TestFlagValidator:
    """Tests for flag validator functions"""

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
        assert FlagValidator.validate_flag_format(flag)

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
        assert not FlagValidator.validate_flag_format(flag)

    @pytest.mark.parametrize(
        "provided_word, actual_word",
        [
            ("flag", "flag"),
            ("kot", "kot"),
            ("pies", "pies"),
            ("Autobus123ZWielkiej", "Autobus123ZWielkiej"),
            ("flag{test_word_1235}", "flag{test_word_1235}"),
            (
                "flag{Makaron_Z_Serem_I_Sosem_Salsa}",
                "flag{Makaron_Z_Serem_I_Sosem_Salsa}",
            ),
            (
                "flag{nazwa_Flagi_Jaka_Chce_123451}",
                "flag{nazwa_Flagi_Jaka_Chce_123451}",
            ),
            (
                "flag{Taka_Dluga_Flaga_Ze_Specjalnymi_znakami_!@$@#^flag@*#^*}",
                "flag{Taka_Dluga_Flaga_Ze_Specjalnymi_znakami_!@$@#^flag@*#^*}",
            ),
        ],
    )
    def test_hashing_algorithm_same_input_have_equal_hashes(
        self, provided_word: str, actual_word: str
    ) -> None:
        """Test flag format check when flag in wrong format provided"""
        assert FlagValidator.compare_word_hashes(provided_word, actual_word)

    @pytest.mark.parametrize(
        "provided_word, actual_word",
        [
            ("flag", "flag123"),
            (
                "TakaDlugaFlagaZeSpecjalnymiznakami!@$@#^flag@*#^*",
                "InnaDlugaFlagaZeSpecjalnymiznakami!@$@#^flag@*#^*",
            ),
            ("flag{test_word}", "flag{other_word}"),
            ("flag{h3v3_4n1c3_d4y}", "flag{123}"),
        ],
    )
    def test_hashing_algorithm_different_input_not_equal_hashes(
        self, provided_word: str, actual_word: str
    ) -> None:
        """Test flag format check when flag in wrong format provided"""
        assert not FlagValidator.compare_word_hashes(provided_word, actual_word)

    @pytest.mark.parametrize(
        "word, md5_word",
        [
            ("flag", "327a6c4304ad5938eaf0efb6cc3e53dc"),
            (
                "TakaDlugaFlagaZeSpecjalnymiznakami!@$@#^flag@*#^*",
                "d66b69a8e881ba6a0c6f4208ad425998",
            ),
            ("123", "202cb962ac59075b964b07152d234b70"),
            ("flag{test_word}", "ec1936de82200b89affbaae27305cfd9"),
        ],
    )
    def test_hash_should_be_equal_to_md5_value(self, word: str, md5_word: str) -> None:
        """Test hashing calculates valid md5 value"""
        assert FlagValidator.hash_to_md5(word) == md5_word
