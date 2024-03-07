"""Validates flags provided by user using md5"""
import hashlib
import re

_FLAG_FORMAT = r"^flag\{[a-z0-9_]*\}"

def validate_flag_format(flag: str) -> bool:
    """Check whether flag matches valid pattern: flag{hidden_text}

    Args:
        flag (str): flag word provided by user

    Returns:
        bool: true if flag matches format
    """
    # flag_pattern = re.compile(_FLAG_FORMAT)
    return re.fullmatch(_FLAG_FORMAT, flag)

def compare_word_hashes(provided_word: str, actual_word: str) -> bool:
    """Compares md5 of two words (case sensitive)

    Args:
        provided_word (str): flag given by user
        actual_word (str): valid word to compare with user input

    Returns:
        bool: true if both words have the same md5 value
    """
    return hash_to_md5(provided_word) == hash_to_md5(actual_word)

def hash_to_md5(word: str) -> str:
    """Returns md5 of given word

    Args:
        word (str): string to hash 

    Returns:
        str: md5 hash of word
    """
    return hashlib.md5(word.encode()).hexdigest()
