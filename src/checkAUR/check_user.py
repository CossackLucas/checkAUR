"""Checking user id
"""

import os


def check_if_root() -> bool:
    """check if user executing the program is the root

    Returns:
        bool: if it's root then True
    """
    if os.getuid() == 0:
        return True
    return False
