"""Flag Validator module"""

import re

_FLAG_FORMAT = r"^flag\{[a-z0-9_]*\}"


class FlagValidator:
    """Validates flags provided by user using md5"""

    def validate_flag_format(self, flag: str) -> bool:
        """Check whether flag matches valid pattern: flag{hidden_text}

        Args:
            flag (str): flag word provided by user

        Returns:
            bool: true if flag matches format
        """
        # flag_pattern = re.compile(_FLAG_FORMAT)
        return re.fullmatch(_FLAG_FORMAT, flag)
