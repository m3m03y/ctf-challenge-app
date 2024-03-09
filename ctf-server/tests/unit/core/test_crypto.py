"""Test cryptography module"""

import pytest
from ctf_server.core.crypto import Crypto


class TestFlagValidator:
    """Tests md5 hashing functions"""

    @pytest.mark.parametrize(
        "provided_word, actual_word",
        [
            ("", ""),
            (" ", " "),
            ("  ", "  "),
            ("word", "word"),
            ("w0rd_w17h_numb3r5", "w0rd_w17h_numb3r5"),
            ("UPPERCASEWORD", "UPPERCASEWORD"),
            ("multiple_parts_word", "multiple_parts_word"),
            ("flag{test_flag}", "flag{test_flag}"),
            ("flag{Very_Long_Test_Flag}", "flag{Very_Long_Test_Flag}"),
            (
                "flag{all_possible_sign_types_used_123}",
                "flag{all_possible_sign_types_used_123}",
            ),
            (
                "flag{Very_Long_Flag_With_Numbers_And_Special_Signs_!@$@#^flag@*#^*}",
                "flag{Very_Long_Flag_With_Numbers_And_Special_Signs_!@$@#^flag@*#^*}",
            ),
        ],
    )
    def test_hashing_algorithm_same_input_have_equal_hashes(
        self, provided_word: str, actual_word: str
    ) -> None:
        """Test flag format check when flag in wrong format provided"""
        assert Crypto.compare_word_hashes(provided_word, actual_word)

    @pytest.mark.parametrize(
        "provided_word, actual_word",
        [
            ("", " "),
            (" ", ""),
            ("word", ""),
            ("      ", "    "),
            ("word", "other_word"),
            ("w0rd_w17h_numb3r5", "diff3r3n7_w0rd_w17h_numb3r5"),
            ("UPPERCASEWORD", "SECONDUPPERCASEWORD"),
            ("multiple_parts_word", "second_multiple_parts_word"),
            ("flag{test_flag}", "flag{other_flag}"),
            ("flag{Very_Long_Test_Flag}", "flag{Short_Flag}"),
            (
                "flag{all_possible_sign_types_used_123}",
                "flag{different_signs_used_849}",
            ),
            (
                "flag{Very_Long_Flag_With_Numbers_And_Special_Signs_!@$@#^flag@*#^*}",
                "",
            ),
        ],
    )
    def test_hashing_algorithm_different_input_not_equal_hashes(
        self, provided_word: str, actual_word: str
    ) -> None:
        """Test flag format check when flag in wrong format provided"""
        assert not Crypto.compare_word_hashes(provided_word, actual_word)

    @pytest.mark.parametrize(
        "word, md5_hash",
        [
            ("", "d41d8cd98f00b204e9800998ecf8427e"),
            (" ", "7215ee9c7d9dc229d2921a40e899ec5f"),
            ("  ", "23b58def11b45727d3351702515f86af"),
            ("word", "c47d187067c6cf953245f128b5fde62a"),
            ("w0rd_w17h_numb3r5", "91d932d97a76016d1f22f688aba16f1b"),
            ("UPPERCASEWORD", "4d2ca5fefa0119c72879a7021468e91e"),
            ("multiple_parts_word", "1e280540cfe19e7a7c0637f0e49f2320"),
            ("flag{test_flag}", "5aff3eee24f45a8f5a4c8e69c3a048b2"),
            ("flag{Very_Long_Test_Flag}", "5e55bbdb3bbbb80d1035ec6686254166"),
            (
                "flag{all_possible_sign_types_used_123}",
                "266efa0426486095ccd24fa1a9dda6b6",
            ),
            (
                "flag{Very_Long_Flag_With_Numbers_And_Special_Signs_!@$@#^flag@*#^*}",
                "c90298488677360d80f242bc223f046e",
            ),
        ],
    )
    def test_provided_word_hash_should_equal_stored_hash_of_same_word(
        self, word: str, md5_hash: str
    ) -> None:
        """Test comparision between plain text and md5 hash value"""
        assert Crypto.compare_word_with_hash(word, md5_hash)

    @pytest.mark.parametrize(
        "word, md5_hash",
        [
            ("", "7215ee9c7d9dc229d2921a40e899ec5f"),
            (" ", "d41d8cd98f00b204e9800998ecf8427e"),
            ("word", "d41d8cd98f00b204e9800998ecf8427e"),
            ("      ", "0cf31b2c283ce3431794586df7b0996d"),
            ("word", "c4fbc587d209f2f6015451d5c0b7b8b6"),
            ("w0rd_w17h_numb3r5", "0972ef07a2e5a39fb0508fbcf2114431"),
            ("UPPERCASEWORD", "4315c4dd872a34cc9ffffdc97864284e"),
            ("multiple_parts_word", "61a8c018e6c885b49484eff03e6787af"),
            ("flag{test_flag}", "a6e203ab6b2a031032ffa6b26ce3ee19"),
            ("flag{Very_Long_Test_Flag}", "cfec73c46f3894873c1ac356aa7f0934"),
            (
                "flag{all_possible_sign_types_used_123}",
                "809cc62d831cf9784db55350ffe13f73",
            ),
            (
                "flag{Very_Long_Flag_With_Numbers_And_Special_Signs_!@$@#^flag@*#^*}",
                "d41d8cd98f00b204e9800998ecf8427e",
            ),
        ],
    )
    def test_provided_word_hash_should_not_equal_stored_hash_of_different_word(
        self, word: str, md5_hash: str
    ) -> None:
        """Test comparision between plain text and invalid md5 hash value"""
        assert not Crypto.compare_word_with_hash(word, md5_hash)

    @pytest.mark.parametrize(
        "word, md5_value",
        [
            ("", "d41d8cd98f00b204e9800998ecf8427e"),
            (" ", "7215ee9c7d9dc229d2921a40e899ec5f"),
            ("  ", "23b58def11b45727d3351702515f86af"),
            ("word", "c47d187067c6cf953245f128b5fde62a"),
            ("w0rd_w17h_numb3r5", "91d932d97a76016d1f22f688aba16f1b"),
            ("UPPERCASEWORD", "4d2ca5fefa0119c72879a7021468e91e"),
            ("multiple_parts_word", "1e280540cfe19e7a7c0637f0e49f2320"),
            ("flag{test_flag}", "5aff3eee24f45a8f5a4c8e69c3a048b2"),
            ("flag{Very_Long_Test_Flag}", "5e55bbdb3bbbb80d1035ec6686254166"),
            (
                "flag{all_possible_sign_types_used_123}",
                "266efa0426486095ccd24fa1a9dda6b6",
            ),
            (
                "flag{Very_Long_Flag_With_Numbers_And_Special_Signs_!@$@#^flag@*#^*}",
                "c90298488677360d80f242bc223f046e",
            ),
        ],
    )
    def test_hash_should_be_equal_to_md5_value(self, word: str, md5_value: str) -> None:
        """Test hashing calculates valid md5 value"""
        assert Crypto.hash_to_md5(word) == md5_value
