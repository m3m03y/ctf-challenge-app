"""MD5 hashing module"""

import hashlib


class Crypto:
    """Handles md5 hashing and word comparasions with hashed words"""

    @classmethod
    def compare_word_hashes(cls, provided_word: str, actual_word: str) -> bool:
        """Compares md5 of two words (case sensitive)

        Args:
            provided_word (str): flag given by user
            actual_word (str): valid word to compare with user input

        Returns:
            bool: true if both words have the same md5 value
        """
        return cls.hash_to_md5(provided_word) == cls.hash_to_md5(actual_word)

    @classmethod
    def hash_to_md5(cls, word: str) -> str:
        """Returns md5 of given word

        Args:
            word (str): string to hash

        Returns:
            str: md5 hash of word
        """
        return hashlib.md5(word.encode()).hexdigest()
